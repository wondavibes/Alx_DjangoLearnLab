from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    ProfileForm,
    PostForm,
    CommentForm,
)
from .models import Post, Comment
from django.db.models import Q
from taggit.models import Tag
from django.conf import settings


class AppLoginView(LoginView):
    template_name = "blog/login.html"


class AppLogoutView(LogoutView):
    template_name = "blog/logout.html"


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            if user:
                login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "blog/profile.html", context)


# CRUD Views for Posts and Comments


class PostListView(ListView):
    """
    Main view to list all blog posts, potentially with pagination.
    """
    model = Post
    queryset = Post.objects.all().order_by('-published_date') 
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10 
    tag = None # Initialize tag attribute

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We only set current_tag if it was set in a subclass (like PostByTagListView)
        if self.tag: 
            context['current_tag'] = self.tag
            context['title'] = f"Posts Tagged: {self.tag.name}"
        else:
            context['title'] = "All Blog Posts"

        return context
    
    # We move the filtering logic to the subclass
    def get_queryset(self):
        return super().get_queryset().distinct()


class PostByTagListView(PostListView):
    """
    Specific view to list posts filtered by a specific tag slug provided in the URL.
    Inherits all base functionality from PostListView.
    """
    def get_queryset(self):
        # Start with the base queryset defined in PostListView
        queryset = super().get_queryset() 
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            # We look up the specific tag dynamically
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            # Filter the posts to only include those associated with that tag
            queryset = queryset.filter(tags__in=[self.tag])
            
        return queryset



class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = context["post"].comments.order_by("-created_at")
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def form_valid(self, form):
        post: Post = get_object_or_404(Post, pk=self.kwargs["post_pk"])  # type: ignore
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added.")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs["post_pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post: Post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        context["post"] = post
        context["comments"] = post.comments.order_by("-created_at")  # type: ignore
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self) -> bool:
        comment: Comment = self.get_object()  # type: ignore
        return self.request.user == comment.author

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully!")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        comment: Comment = self.get_object()  # type: ignore
        return reverse_lazy("post_detail", kwargs={"pk": comment.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self) -> bool:
        comment: Comment = self.get_object()  # type: ignore
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Comment deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self) -> str:
        comment: Comment = self.get_object()  # type: ignore
        return reverse_lazy("post_detail", kwargs={"pk": comment.post.pk})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def test_func(self) -> bool:
        post: Post = self.get_object()  # type: ignore
        return self.request.user == post.author

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, "You can only edit your own posts.")
        return redirect("post_detail", pk=self.get_object().pk)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def test_func(self) -> bool:
        post: Post = self.get_object()  # type: ignore
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "You can only delete your own posts.")
        return redirect("post_detail", pk=self.get_object().pk)


def post_search(request):
    query = request.GET.get("q")
    results = Post.objects.all()

    if query:
        # Use Q objects to search title OR content OR tags
        results = results.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)  # Search within the tag names
        ).distinct()  # Use distinct() to avoid duplicate posts if they match multiple criteria

    context = {
        "query": query,
        "posts": results,
    }
    return render(request, "blog/search_results.html", context)


def post_list_by_tag(request, tag_slug):
    tag = get_object_or_404(
        Tag, slug=tag_slug
    )  # Get the specific tag object (Note: Tag model is dynamic)
    posts = Post.objects.filter(tags__in=[tag])  # Filter posts that have this tag

    context = {
        "tag": tag,
        "posts": posts,
    }
    return render(request, "blog/post_list_by_tag.html", context)

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import TaskForm, ProfileForm, SignupForm
from .models import Task, Category, Profile

def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        return redirect("task_list")
    return render(request, "registration/signup.html", {"form": form})

@login_required
def task_list(request):
    qs = request.user.tasks.select_related("category")
    q, cat, status = request.GET.get("q", ""), request.GET.get("cat", ""), request.GET.get("status", "")
    if q: qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if cat: qs = qs.filter(category_id=cat)
    if status == "done": qs = qs.filter(is_done=True)
    elif status == "todo": qs = qs.filter(is_done=False)
    page = Paginator(qs, 10).get_page(request.GET.get("page"))
    stats = {"total": request.user.tasks.count(), "done": request.user.tasks.filter(is_done=True).count()}
    return render(request, "tasks/task_list.html", {
        "page": page, "q": q, "cat": cat, "status": status, "stats": stats,
        "categories": request.user.category_set.all()})

@login_required
def task_edit(request, pk=None):
    task = get_object_or_404(Task, pk=pk, user=request.user) if pk else None
    form = TaskForm(request.POST or None, instance=task, user=request.user)
    if form.is_valid():
        t = form.save(commit=False)
        t.user = request.user
        if "remind_at" in form.changed_data: t.reminded = False
        t.save()
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"form": form, "task": task})

@login_required
@require_POST
def task_toggle(request, pk):
    t = get_object_or_404(Task, pk=pk, user=request.user)
    t.is_done = not t.is_done
    t.save(update_fields=["is_done"])
    return redirect(request.META.get("HTTP_REFERER", "task_list"))

@login_required
@require_POST
def task_delete(request, pk):
    get_object_or_404(Task, pk=pk, user=request.user).delete()
    return redirect("task_list")

@login_required
@require_POST
def category_add(request):
    name = request.POST.get("name", "").strip()
    if name: Category.objects.get_or_create(user=request.user, name=name)
    return redirect("task_list")

@login_required
def profile(request):
    obj, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=obj)
    saved = False
    if form.is_valid(): form.save(); saved = True
    return render(request, "tasks/profile.html", {"form": form, "saved": saved})

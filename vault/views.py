from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from .forms import RecipeForm, IngredientForm, MealPlanForm
from .models import Recipe, Ingredient, MealPlan

def _user_is_premium(user) -> bool:
    if not user.is_authenticated:
        return False
    try:
        return user.profile.is_premium
    except Profile.DoesNotExist:
        return False

def recipe_list(request):
    query = request.GET.get("q", "").strip()
    base = Recipe.objects.all()

    # Public: show non-premium recipes (and premium only if user is premium)
    if _user_is_premium(request.user):
        visible = base
    else:
        visible = base.filter(is_premium=False)

    if query:
        visible = visible.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, "vault/recipe_list.html", {"recipes": visible, "q": query})

def recipe_detail(request, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.is_premium and not _user_is_premium(request.user):
        messages.warning(request, "This is a Premium recipe. Upgrade to access it.")
        return redirect("payments:pricing")

    return render(request, "vault/recipe_detail.html", {"recipe": recipe})

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            messages.success(request, "Recipe created.")
            return redirect("vault:recipe_edit", pk=recipe.pk)
        messages.error(request, "Please fix the errors in the form.")
    else:
        form = RecipeForm()
    return render(request, "vault/recipe_form.html", {"form": form, "mode": "create"})

@login_required
def recipe_edit(request, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        ingredient_form = IngredientForm(request.POST)

        if "save_recipe" in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "Recipe updated.")
                return redirect("vault:recipe_edit", pk=pk)
            messages.error(request, "Please fix the recipe form errors.")

        if "add_ingredient" in request.POST:
            if ingredient_form.is_valid():
                ing = ingredient_form.save(commit=False)
                ing.recipe = recipe
                ing.save()
                messages.success(request, "Ingredient added.")
                return redirect("vault:recipe_edit", pk=pk)
            messages.error(request, "Please fix the ingredient form errors.")
    else:
        form = RecipeForm(instance=recipe)
        ingredient_form = IngredientForm()

    return render(request, "vault/recipe_form.html", {
        "form": form,
        "ingredient_form": ingredient_form,
        "recipe": recipe,
        "mode": "edit",
    })

@login_required
def ingredient_delete(request, pk: int):
    ing = get_object_or_404(Ingredient, pk=pk, recipe__owner=request.user)
    recipe_id = ing.recipe_id
    if request.method == "POST":
        ing.delete()
        messages.info(request, "Ingredient removed.")
        return redirect("vault:recipe_edit", pk=recipe_id)
    raise Http404()

@login_required
def recipe_delete(request, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == "POST":
        recipe.delete()
        messages.info(request, "Recipe deleted.")
        return redirect("vault:recipe_list")
    return render(request, "vault/recipe_confirm_delete.html", {"recipe": recipe})

@login_required
def mealplan_list(request):
    plans = MealPlan.objects.filter(owner=request.user)
    return render(request, "vault/mealplan_list.html", {"plans": plans})

@login_required
def mealplan_detail(request, pk: int):
    plan = get_object_or_404(MealPlan, pk=pk, owner=request.user)

    # Defensive: if plan references premium recipes, ensure access
    if not _user_is_premium(request.user) and plan.recipes.filter(is_premium=True).exists():
        messages.warning(request, "This plan includes Premium recipes. Upgrade to view them.")
        return redirect("payments:pricing")

    return render(request, "vault/mealplan_detail.html", {"plan": plan})

@login_required
def mealplan_create(request):
    if request.method == "POST":
        form = MealPlanForm(request.POST)
        form.fields["recipes"].queryset = Recipe.objects.filter(owner=request.user)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.owner = request.user
            plan.save()
            form.save_m2m()
            messages.success(request, "Meal plan created.")
            return redirect("vault:mealplan_detail", pk=plan.pk)
        messages.error(request, "Please fix the errors in the form.")
    else:
        form = MealPlanForm(initial={"week_start": date.today()})
        form.fields["recipes"].queryset = Recipe.objects.filter(owner=request.user)

    return render(request, "vault/mealplan_form.html", {"form": form, "mode": "create"})

@login_required
def mealplan_edit(request, pk: int):
    plan = get_object_or_404(MealPlan, pk=pk, owner=request.user)

    if request.method == "POST":
        form = MealPlanForm(request.POST, instance=plan)
        form.fields["recipes"].queryset = Recipe.objects.filter(owner=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Meal plan updated.")
            return redirect("vault:mealplan_detail", pk=plan.pk)
        messages.error(request, "Please fix the errors in the form.")
    else:
        form = MealPlanForm(instance=plan)
        form.fields["recipes"].queryset = Recipe.objects.filter(owner=request.user)

    return render(request, "vault/mealplan_form.html", {"form": form, "mode": "edit"})

@login_required
def mealplan_delete(request, pk: int):
    plan = get_object_or_404(MealPlan, pk=pk, owner=request.user)
    if request.method == "POST":
        plan.delete()
        messages.info(request, "Meal plan deleted.")
        return redirect("vault:mealplan_list")
    return render(request, "vault/mealplan_confirm_delete.html", {"plan": plan})

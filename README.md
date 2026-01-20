# MealVault

A full-stack Django web application for saving recipes and building weekly meal plans. Users authenticate to persist their data. Premium recipes are protected behind Stripe test payments.

## Target Audience
Home cooks and busy people who want to plan meals quickly and reuse a personal recipe vault.

## Value Provided
- Users can create and manage recipes and meal plans (CRUD).
- Premium recipes are locked behind payment and cannot be accessed by anonymous or unpaid users.
- The business owner can monetise premium recipe packs via Stripe.

## Tech Stack
- Django (Python)
- HTML/CSS/Bootstrap
- JavaScript (live ingredient scaling)
- PostgreSQL (recommended for production)
- Stripe (test mode)

## Apps
- `core` — marketing pages
- `accounts` — authentication + Profile (premium access flag)
- `vault` — Recipe + Ingredient + MealPlan models and CRUD
- `payments` — Stripe checkout + webhook activation

## Data Schema
### Recipe
- owner (FK -> User)
- title, description, servings
- is_premium
- created_at

### Ingredient
- recipe (FK -> Recipe)
- name, quantity, unit

### MealPlan
- owner (FK -> User)
- name, notes, week_start
- recipes (M2M -> Recipe)

Relationships:
- One user owns many Recipes and MealPlans.
- One Recipe has many Ingredients.
- MealPlan contains many Recipes.

## Permissions & Security
- Only owners can edit/delete their recipes and meal plans (view-level filtering).
- Premium content is gated: if recipe.is_premium and user not premium -> redirected to pricing.
- Secrets are stored in env vars (.env not committed).
- DEBUG disabled in production.

## Stripe Payment Flow
1. User clicks Premium -> Checkout
2. Stripe redirects to success/cancel
3. Webhook `checkout.session.completed` sets `Profile.is_premium=True`

## Testing
- Django TestCase tests for core pages
- Owner permissions tests for CRUD
- Payments pricing page test
Run:
```bash
python manage.py test

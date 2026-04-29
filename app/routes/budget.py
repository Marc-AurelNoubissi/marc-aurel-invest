from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Budget, Transaction

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budgets')
@login_required
def liste():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()

    # Pour chaque budget, calculer les dépenses réelles
    budgets_avec_stats = []
    for b in budgets:
        depenses_reelles = sum(
            t.montant for t in Transaction.query.filter_by(
                user_id=current_user.id,
                type='depense',
                categorie=b.categorie
            ).all()
            if t.date.month == b.mois and t.date.year == b.annee
        )
        pourcentage = min(round((depenses_reelles / b.limite) * 100), 100) if b.limite > 0 else 0

        if pourcentage >= 100:
            statut = 'danger'
            icone = '🔴'
        elif pourcentage >= 75:
            statut = 'warning'
            icone = '⚠️'
        else:
            statut = 'success'
            icone = '✅'

        budgets_avec_stats.append({
            'id': b.id,
            'categorie': b.categorie,
            'limite': b.limite,
            'mois': b.mois,
            'annee': b.annee,
            'depenses_reelles': depenses_reelles,
            'pourcentage': pourcentage,
            'statut': statut,
            'icone': icone,
            'restant': b.limite - depenses_reelles
        })

    return render_template('budget/liste.html', budgets=budgets_avec_stats)

@budget_bp.route('/budgets/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    if request.method == 'POST':
        nouveau = Budget(
            categorie=request.form.get('categorie'),
            limite=float(request.form.get('limite')),
            mois=int(request.form.get('mois')),
            annee=int(request.form.get('annee')),
            user_id=current_user.id
        )
        db.session.add(nouveau)
        db.session.commit()
        flash('Budget ajouté avec succès !', 'success')
        return redirect(url_for('budget.liste'))

    return render_template('budget/ajouter.html')

@budget_bp.route('/budgets/supprimer/<int:id>')
@login_required
def supprimer(id):
    budget = Budget.query.get_or_404(id)
    if budget.user_id != current_user.id:
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('budget.liste'))
    db.session.delete(budget)
    db.session.commit()
    flash('Budget supprimé.', 'success')
    return redirect(url_for('budget.liste'))
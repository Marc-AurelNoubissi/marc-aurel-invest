from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Transaction
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions')
@login_required
def liste():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('transactions/liste.html', transactions=transactions)

@transactions_bp.route('/transactions/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    if request.method == 'POST':
        nouvelle = Transaction(
            titre=request.form.get('titre'),
            montant=float(request.form.get('montant')),
            type=request.form.get('type'),
            categorie=request.form.get('categorie'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
            note=request.form.get('note'),
            user_id=current_user.id
        )
        db.session.add(nouvelle)
        db.session.commit()
        flash('Transaction ajoutée avec succès !', 'success')
        return redirect(url_for('transactions.liste'))

    return render_template('transactions/ajouter.html')

@transactions_bp.route('/transactions/supprimer/<int:id>')
@login_required
def supprimer(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('transactions.liste'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction supprimée.', 'success')
    return redirect(url_for('transactions.liste'))
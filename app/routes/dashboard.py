from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Transaction, Budget
import plotly.graph_objs as go
import plotly.offline as pyo

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(5).all()
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    toutes = Transaction.query.filter_by(user_id=current_user.id).all()

    revenus = sum(t.montant for t in toutes if t.type == 'revenu')
    depenses = sum(t.montant for t in toutes if t.type == 'depense')
    solde = revenus - depenses

    # Graphique 1 : Donut Revenus vs Dépenses
    fig1 = go.Figure(data=[go.Pie(
        labels=['Revenus', 'Dépenses'],
        values=[revenus or 1, depenses or 1],
        hole=0.55,
        marker=dict(colors=['#22c55e', '#ef4444']),
        textinfo='label+percent'
    )])
    fig1.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False, height=250
    )

    # Graphique 2 : Dépenses par catégorie
    categories = {}
    for t in toutes:
        if t.type == 'depense':
            categories[t.categorie] = categories.get(t.categorie, 0) + t.montant

    fig2 = go.Figure(data=[go.Bar(
        x=list(categories.keys()) or ['Aucune'],
        y=list(categories.values()) or [0],
        marker_color='#7c3aed'
    )])
    fig2.update_layout(
        margin=dict(t=20, b=40, l=40, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=250
    )

    # Graphique 3 : Évolution du solde
    toutes_triees = sorted(toutes, key=lambda t: t.date)
    dates, soldes, cumul = [], [], 0
    for t in toutes_triees:
        cumul += t.montant if t.type == 'revenu' else -t.montant
        dates.append(t.date.strftime('%d/%m'))
        soldes.append(cumul)

    fig3 = go.Figure(data=[go.Scatter(
        x=dates or ['Aujourd\'hui'],
        y=soldes or [0],
        mode='lines+markers',
        line=dict(color='#7c3aed', width=3),
        fill='tozeroy',
        fillcolor='rgba(124,58,237,0.1)'
    )])
    fig3.update_layout(
        margin=dict(t=20, b=40, l=40, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=250
    )

    # Génération HTML sans CDN externe
    graph1 = pyo.plot(fig1, output_type='div', include_plotlyjs='cdn')
    graph2 = pyo.plot(fig2, output_type='div', include_plotlyjs=False)
    graph3 = pyo.plot(fig3, output_type='div', include_plotlyjs=False)

    return render_template('dashboard/index.html',
        transactions=transactions,
        budgets=budgets,
        revenus=revenus,
        depenses=depenses,
        solde=solde,
        graph1=graph1,
        graph2=graph2,
        graph3=graph3
    )
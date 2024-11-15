from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Agent

agents = Blueprint('agents', __name__)

@agents.route('/agents')
def agent_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_agents = Agent.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('agent/agent_list.html', agents=paginated_agents.items, pagination=paginated_agents)

@agents.route('/agent/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        full_name = request.form['full_name']
        report_id = request.form['report_id']

        new_agent = Agent(full_name=full_name, report_id=report_id)
        db.session.add(new_agent)
        db.session.commit()
        flash('New agent successfully created!')
        return redirect(url_for('agents.agent_list'))

    return render_template('agent/add_agent.html')

@agents.route('/agent/update/<int:agent_id>', methods=['GET', 'POST'])
def update_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)

    if request.method == 'POST':
        agent.full_name = request.form['full_name']
        agent.report_id = request.form['report_id']

        db.session.commit()
        flash('Agent successfully updated!')
        return redirect(url_for('agents.agent_list'))

    return render_template('agent/update_agent.html', agent=agent)

@agents.route('/agent/delete/<int:agent_id>', methods=['POST'])
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    flash('Agent successfully deleted!')
    return redirect(url_for('agents.agent_list'))

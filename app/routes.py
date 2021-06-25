from app import app
from flask import render_template, flash
from app.forms import UserAddressForm
from app import network
from app import user_account


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index_page():
    form = UserAddressForm()
    day = network.getDay()
    network_info = network.networkData()
    new_user_account = user_account.user_account()

    if form.validate_on_submit():
        if new_user_account.updateUser(form.ICX_wallet_address.data, network_info[0], day):
            return render_template('index.html', form=form, user=new_user_account, networkInfo=network_info)

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='info')
    return render_template('index.html', form=form, user=new_user_account, networkInfo=network_info)

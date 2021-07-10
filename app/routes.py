from app import app
import crochet
crochet.setup()  # initialize crochet before further imports
from flask import render_template, flash, jsonify, redirect
from app.forms import UserAddressForm
from app import network
from app import user_account
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scraping.scraping.spiders import scrapingTxHistory
import os
import pytz
from datetime import datetime

tx_data = []
crawl_runner = CrawlerRunner()


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index_page():
    form = UserAddressForm()
    day = network.getDay()
    network_info = network.networkData()
    new_user_account = user_account.user_account()

    if form.validate_on_submit():
            new_user_account.updateUser(form.ICX_wallet_address.data, day)
            scrape(form.ICX_wallet_address.data)
            calculate_tx_age()
            new_user_account.updateUserClaim(tx_data, network_info[0])
            return render_template('index.html', form=form, user=new_user_account, networkInfo=network_info, txData=tx_data)

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='info')
    return render_template('index.html', form=form, user=new_user_account, networkInfo=network_info)


def scrape(wallet_address):
    tx_data.clear()
    # run crawler in twisted reactor synchronously
    scrape_with_crochet(address=wallet_address)
    if os.path.exists("outputfile.json"):
        os.remove("outputfile.json")
    return jsonify(tx_data)


@crochet.wait_for(timeout=60.0)
def scrape_with_crochet(address):
    # signal fires when single item is processed
    # and calls _crawler_result to append that item
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(
        scrapingTxHistory.TxSpider, address = address)
    return eventual  # returns a twisted.internet.defer.Deferred


def _crawler_result(item):
    tx_data.append(dict(item))


def calculate_tx_age():
    for i in range(len(tx_data)):
        date_string = tx_data[i]["date"]
        date_object = datetime.strptime(date_string[:19], "%Y-%m-%dT%H:%M:%S")
        age_delta = datetime.utcnow().replace(tzinfo=pytz.utc) - date_object.replace(tzinfo=pytz.utc)
        if int(age_delta.seconds / 3600) <= 1:
            hourString = " hour"
        else:
            hourString = " hours"
        age = str(age_delta.days) + " days " + str(int(age_delta.seconds / 3600)) + hourString + " ago"
        tx_data[i]["date"] = age


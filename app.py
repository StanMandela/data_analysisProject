from flask import Flask, render_template, request, redirect, url_for,flash

import pygal

import psycopg2

from flask_sqlalchemy import SQLAlchemy
from Config.Config import Development

app = Flask(__name__)

 #import the configs
app.config.from_object(Development)
"""the below code blow has been done with """
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@127.0.0.1:5432/sales_demo'
# app.config['SECRET_KEY'] = 'KenyaYetuMoja'
# app.config['DEBUG'] = True
db = SQLAlchemy(app)


from models.inventories import Inventories
from models.sales import Sales

@app.before_first_request
def create_tables():
    db.create_all()


"""
passing values through a route
1.create the route
<id>- the id no. that to be passed
the func also gets that that id the system will get
every sale you make will be for a specific product.. 
-----------------------------
passing strings
app.route('/test/<name>')
def test(name):
    return name
----------------------
@app.route('/test/<num1>/<num2>')
def test(num1,num2):
    print( int(num1)+int(num2))
    return 'yes'
    returns the answer in the console
"""
# @app.route('/test/<num1>/<num2>')
# def test(num1,num2):
#     print( int(num1)+int(num2))
#     return 'yes'

#creating a delete route
@app.route('/delete/<int:id>')
def delete(id):
    # print(id)
    record=Inventories.fetch_one_record(id)
    # print(record.name)

    db.session.delete(record)
    db.session.commit()

    flash('You have succesfully deleted the inventory','danger')
    return redirect(url_for('hello_world'))

@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit(id):
    record=Inventories.fetch_one_record(id)

    if request.method == 'POST':
        record.name=request.form['Name']
        record.type = request.form['type']
        record.buying_price = request.form['bp']
        record.selling_price = request.form['sp']
        record.stock = request.form['Stock']

        db.session.commit()

        return redirect(url_for('hello_world'))

    return render_template('edit.html',record=record)

@app.route('/salepro/<int:id>',methods=['POST','GET'])
def salez(id):

    record=Inventories.fetch_one_record(id)
    # print(id)
    # return 'T'
    if record:
        if request.method == 'POST':

            quantity=request.form['Quantity']
            newStock=record.stock-int(quantity)

            print(quantity)
            # print(newStock)
            record.stock =newStock
            db.session.commit()

            #Updating to the sales table
            sales=Sales(inv_id=id,quantity=quantity)

            sales.add_records()

            #mideule to notify sale of an item
            flash('You Successfuly made a Sale','success')

        return redirect(url_for('hello_world'))


@app.route('/viewsales/<int:id>')
def viewSales(id):
    print(id)

    record=Inventories.fetch_one_record(id)

    return render_template('sales.html',record=record)

@app.route('/')
def hello_world():
    x='stan'
    records=Inventories.fetch_all_records()

    return render_template('index.html',records=records,x=x)



@app.route('/add_inventory', methods=['POST', 'GET'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['Name']
        type = request.form['type']
        buying_price = request.form['bp']
        selling_price = request.form['sp']
        stock = request.form['Stock']

        # print(name)
        # print(type)
        # print(buying_price)
        # print(selling_price)

        record = Inventories(name=name, type=type , buying_price=buying_price, selling_price=selling_price, stock=stock)
        record.add_records()

    # return 'Stan'
    return redirect(url_for('hello_world'))

#
# @app.route('/dashboard')
# def pie_chart():
#
#     conn = psycopg2.connect("dbname='sales_demo' user='postgres' host='localhost' password='Nancy22*'")
#
#     cur = conn.cursor()
#
#     cur.execute ("""SELECT to_char(to_timestamp (date_part('month', s.created_at)::text, 'MM'), 'Month'), sum(i.selling_price * s.quantity)
# FROM public.inventories as i
# join sales as s on s.inventory_id = i.id
# group by EXTRACT(MONTH FROM s.created_at)
# order by EXTRACT(MONTH FROM s.created_at) asc
# """)
#
#     rows = cur.fetchall()
#     #print(type(rows))
#     x_axis=[]
#     y_axis=[]
#
#     for each in rows:
#         x_axis.append(each[0])
#         y_axis.append(each[1])
#     # print(x_axis)
#     # print(y_axis)
#         #print(each)
#
#
#     # pie_chart = pygal.Pie(inner_radius=.4)
#     # pie_chart.title = 'Browser usage in February 2012 (in %)'
#     # pie_chart.add('IE', 19.5)
#     # pie_chart.add('Firefox', 36.6)
#     # pie_chart.add('Chrome', 36.3)
#     # pie_chart.add('Safari', 4.5)
#     # pie_chart.add('Opera', 2.3)
#     # pie_data = pie_chart.render_data_uri()
#     # return render_template('dashboard.html',pie_data=pie_data)
#
#     # graph = pygal.Line()
#     # graph.title = 'Monthly Sales'
#     # graph.x_labels = x_axis
#     # graph.add('Total Sales', y_axis)
#
#     graph_data = graph.render_data_uri()
#
#     return render_template('dashboard.html', graph_data=graph_data)


if __name__ == '__main__':
    app.run()
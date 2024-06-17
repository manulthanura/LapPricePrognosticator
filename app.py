from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

def prediction(lst):
    filename = "model/predictor.pickle"
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred = model.predict([lst])
    return pred

@app.route('/', methods=[ 'POST','GET'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpu']
        gpu = request.form['gpu']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')

        # print the values
        # print(ram, weight, company, typename, opsys, cpu, gpu, touchscreen, ips)

        # convert the values to a array
        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))
        
        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
        typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
        opsys_list = ['linux', 'mac', 'other', 'windows']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']

        def traverse(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)

        # print(feature_list)
        # Call the model to predict the price
        pred = prediction(feature_list)
        pred = np.round(pred[0], 2)
        # print(pred)
        
    return render_template('index.html', pred=pred)


if __name__ == '__main__':
    # python app.py
    # debug
    # app.run(debug=True)
    # production
    app.run()
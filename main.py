import os
import io
from dotenv import load_dotenv
from flask import Flask, render_template,url_for,Response,request
from forms import UploadCSVForm,ValueForm
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable



load_dotenv()
GEOJASON_PATH="data/N03-20250101_22.geojson"


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_KEY")

@app.route('/')
def show_index():
    return render_template("index.html")

@app.route('/data_entry/<csv>', methods=['GET'])
def data_entry(csv):
    form = UploadCSVForm()
    csv = csv
    return render_template("data_entry.html", form=form,csv=csv)

@app.route('/process_file', methods=['POST'])
def process_file():
    form = UploadCSVForm()
    if form.validate_on_submit():
        uploaded_file = form.file.data
        print("Csv processing")

        df = pd.read_csv(uploaded_file)
        gdf = gpd.read_file(GEOJASON_PATH)
        merged = gdf.merge(df,left_on="N03_004", right_on="自治体名")

        buf = io.BytesIO()

        # 作画
        fig, ax = plt.subplots(1, 1,figsize=(12,8),dpi=200)
        divider = make_axes_locatable(ax)
        plt.title(form.title.data)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        ax.tick_params(bottom=False, left=False, right=False, top=False)
        merged.plot(column=form.values.data,
                    cax=cax,
                    ax=ax,
                    legend=True,
                    legend_kwds={"label": form.title.data},
                    cmap="OrRd")

        fig.savefig(buf,format="png")
        plt.close(fig)
        return Response(buf.getvalue(), mimetype="image/png")
    else:
        return render_template("data_entry.html", form=form, csv=request.form.get("csv"))

if __name__ == '__main__':
    app.run()


#------------------------ カスタム用-------------------------#
# ファイルパス
GEOJASON_PATH="data/N03-20250101_22.geojson"
DATA_FILE_PATH="data/furusato_shizuoka_mock.csv"

# GeoJson側の設定 left_onでマージするコラム名を入力
Geo_Municipalities = "N03_004"

# データ側の設定　right_onでマージするコラム名、可視化する変数の入ったをコラム名入力
DATA_Municipalities = "自治体名"
DATA_COLUMN="収入額（千円）"

# 保存する画像の名前を設定 main.pyのあるフォルダに保存されます
IMAGE_NAME = 'sample.png'

#----------------------------------------------------------#

class ShizuokaMapCreator():
    def __init__(self,geo_municipalities="N03_004",data_municipalities="自治体名"):
        self.geo_municipalities = geo_municipalities
        self.data_municipalities = data_municipalities

    def create_map(self,csv_file,column,title="SAMPLE"):
        df = pd.read_csv(csv_file)
        gdf = gpd.read_file(GEOJASON_PATH)

        # データをマージ
        merged = gdf.merge(df, left_on=self.geo_municipalities, right_on=self.data_municipalities)

        # 作画
        fig, ax = plt.subplots(1, 1)
        divider = make_axes_locatable(ax)
        plt.title(title)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        ax.tick_params(bottom=False, left=False, right=False, top=False)
        merged.plot(column=column,
                    cax=cax,
                    ax=ax,
                    legend=True,
                    legend_kwds={"label": "Revenue"},
                    cmap="OrRd")
        plt.savefig(IMAGE_NAME)
        plt.show()




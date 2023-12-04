from flask import Flask, render_template, Response
import pandas as pd
import pygsheets
import cv2

app = Flask(__name__)

feed = cv2.VideoCapture(0)
qcd = cv2.QRCodeDetector()
auth = pygsheets.authorize(service_file="creds.json")
sheet = auth.open("Robotics Take Home Test")
page = sheet[0]


def scanBarcode(feed):
    barcodeData = []
    gotInfo, decodedInfo, points, _ = qcd.detectAndDecodeMulti(feed)
    if gotInfo:
        for info, points in zip(decodedInfo, points):
            if info:
                print(info)
                color = (0, 255, 0)  # Green
                barcodeData.append(info)
                cv2.putText(
                    feed,
                    "QR Code Scanned Succesfully!",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_4,
                )
            else:
                color = (0, 0, 255)  # Red

            feed = cv2.polylines(feed, [points.astype(int)], True, color, 10)

        if barcodeData != [""]:
            previousData = set(list(page.get_as_df()["Barcode Values"]))
            previousData.update(barcodeData)
            updatedData = list(previousData)
            df = pd.DataFrame({"Barcode Values": updatedData})
            page.set_dataframe(df, (1, 1))

    return feed


def getFeed():
    while True:
        frame = scanBarcode(feed.read()[1])
        buffer = cv2.imencode(".jpg", frame)[1]
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/get-values/")
def getValues():
    previousData = list(page.get_as_df()["Barcode Values"])
    return render_template("displayValues.html", barcodes=previousData)


@app.route("/live-feed/")
def liveFeed():
    return Response(getFeed(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)

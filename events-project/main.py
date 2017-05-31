from flask import Flask, render_template, request, Response
import json, csv, os

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
    )

@app.route("/", methods=["GET", "POST"])
def main():
    with open("db.json", mode="r") as json_file:
        feeds = json.load(json_file)
    if request.method == "POST":
        event_name = request.form["event_name"]
        email = request.form["email"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        for pos, val in enumerate(feeds):
            if feeds[pos]["event_name"] == event_name:
                feeds.pop(pos)
                break
        with open("db.json", mode="w") as json_file:
            entry = { 'event_name': event_name,
                      'email': email,
                      'start_date': start_date,
                      'end_date': end_date,
                      'member': list()
                    }
            feeds.append(entry)
            json.dump(feeds, json_file)
    return render_template('index.html', events=feeds)

@app.route("/events/<event_name>", methods=["GET"])
def view_event(event_name=None):
    return render_template('events.html', event_name=event_name)

@app.route("/join", methods=["POST"])
def join_event():
    if request.method == "POST":
        member_name = request.form["member_name"]
        event_name = request.form["event_name"]
        print event_name
        with open("db.json", mode="r") as json_file:
            feeds = json.load(json_file)
        for feed in feeds:
            if feed["event_name"] == event_name:
                feed["member"].append(member_name)
                break
        with open("db.json", mode="w") as json_file:
            json.dump(feeds, json_file)
        return render_template('index.html', events=feeds)

@app.route("/remove/<event_name>", methods=["GET"])
def remove_event(event_name=None):
    if not event_name == None:
        with open("db.json", mode="r") as json_file:
            feeds = json.load(json_file)
        for pos, val in enumerate(feeds):
            if feeds[pos]["event_name"] == event_name:
                feeds.pop(pos)
                break
        with open("db.json", mode="w") as json_file:
            json.dump(feeds, json_file)
    return render_template('index.html', events=feeds)

@app.route("/download_csv/<event_name>", methods=["GET"])
def download_csv(event_name=None):
    with open("db.json", mode="r") as json_file:
        feeds = json.load(json_file)
    if not event_name == None:
        for feed in feeds:
            if feed["event_name"] == event_name:
                csv = ','.join(feed["member"])
                return Response(
                    csv,
                    mimetype="text/csv",
                    headers={"Content-disposition":
                             "attachment; filename=%s.csv" % (feed["event_name"])}
                    )
    return render_template('index.html', events=feeds)


@app.route("/create_event", methods=["GET"])
def create_event():
    return render_template('create_event.html')

@app.route("/about_me", methods=["GET"])
def show_about_me():
    return render_template('about_me.html')

if __name__ == "__main__":
    app.run(debug=True)

import csv
from flask import Flask, request, render_template_string


app = Flask(__name__)


students = {}
student_ids = {}
hw1_scores = {}
hw2_scores = {}
next_id = 1


with open("hw-01.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")

    for row in reader:
        name = row["Имя"]
        group_id = int(row["Группа"])
        score = float(row["Баллы"])

        key = (name, group_id)

        if key not in student_ids:
            student_ids[key] = next_id
            students[next_id] = {"name": name, "group_id": group_id}
            next_id += 1

        student_id = student_ids[key]
        hw1_scores[student_id] = score


with open("hw-02.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")

    for row in reader:
        name = row["Имя"]
        group_id = int(row["Группа"])
        score = float(row["Баллы"])

        key = (name, group_id)

        if key not in student_ids:
            student_ids[key] = next_id
            students[next_id] = {"name": name, "group_id": group_id}
            next_id += 1

        student_id = student_ids[key]
        hw2_scores[student_id] = score
def get_mark(score):
    if score < 1:
        return 2
    if score < 30:
        return 3
    if score < 50:
        return 4
    return 5


@app.route("/names")
def names():
    result = []

    for student_id in students:
        result.append(students[student_id]["name"])

    return {"names": result}


@app.route("/<hw_name>/mean_score")
def hw_mean_score(hw_name):
    if hw_name == "hw-01":
        scores = hw1_scores
    elif hw_name == "hw-02":
        scores = hw2_scores
    else:
        return {"error": "no such hw or no scores"}, 400

    total = 0
    count = 0

    for student_id, score in scores.items():
        total += score
        count += 1

    if count == 0:
        return {"error": "no such hw or no scores"}, 400

    return {"mean_score": total / count}


@app.route("/<hw_name>/<int:group_id>/mean_score")
def hw_group_mean_score(hw_name, group_id):
    if hw_name == "hw-01":
        scores = hw1_scores
    elif hw_name == "hw-02":
        scores = hw2_scores
    else:
        return {"error": "no such group or no scores"}, 400

    total = 0
    count = 0

    for student_id, score in scores.items():
        if students[student_id]["group_id"] == group_id:
            total += score
            count += 1

    if count == 0:
        return {"error": "no such group or no scores"}, 400

    return {"mean_score": total / count}


@app.route("/mean_score/")
def mean_score():
    hw_name = request.args.get("hw_name")
    group_id = request.args.get("group_id")

    if hw_name is None or group_id is None:
        return {"error": "no hw_name or group_id"}, 400

    if hw_name == "hw-01":
        scores = hw1_scores
    elif hw_name == "hw-02":
        scores = hw2_scores
    else:
        return {"error": "no such group or no scores"}, 400

    total = 0
    count = 0

    for student_id, score in scores.items():
        if students[student_id]["group_id"] == int(group_id):
            total += score
            count += 1

    if count == 0:
        return {"error": "no such group or no scores"}, 400

    return {"mean_score": total / count}


@app.route("/mark")
def mark():
    student_id = request.args.get("student_id")
    group_id = request.args.get("group_id")

    if student_id is not None:
        student_id = int(student_id)
        total_score = hw1_scores.get(student_id, 0) + hw2_scores.get(student_id, 0)
        return {"mark": get_mark(total_score)}

    if group_id is not None:
        group_id = int(group_id)
        marks = []

        for student_id in students:
            if students[student_id]["group_id"] == group_id:
                total_score = hw1_scores.get(student_id, 0) + hw2_scores.get(student_id, 0)
                marks.append(get_mark(total_score))

        if len(marks) == 0:
            return {"error": "no such group"}, 400

        return {"mean_mark": sum(marks) / len(marks)}

    return {"error": "no student_id or group_id"}, 400


@app.route("/course_table/")
def course_table():
    hw_name = request.args.get("hw_name")
    group_id = request.args.get("group_id")

    if hw_name is None:
        return {"error": "no hw_name"}, 400

    if hw_name == "hw-01":
        scores = hw1_scores
    elif hw_name == "hw-02":
        scores = hw2_scores
    else:
        return {"error": "no such hw"}, 400

    rows = []

    for student_id in students:
        if group_id is not None and students[student_id]["group_id"] != int(group_id):
            continue

        rows.append({
            "name": students[student_id]["name"],
            "group_id": students[student_id]["group_id"],
            "score": scores.get(student_id, 0)
        })

    html = """
    <html>
    <body>
        <h2>{{ hw_name }}</h2>
        <table border="1">
            <tr>
                <th>name</th>
                <th>group</th>
                <th>score</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row["name"] }}</td>
                <td>{{ row["group_id"] }}</td>
                <td>{{ row["score"] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html, hw_name=hw_name, rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)

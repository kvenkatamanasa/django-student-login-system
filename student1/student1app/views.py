from django.shortcuts import render
import pymysql


def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='student'
    )


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":

        username = request.POST.get("t1")
        password = request.POST.get("t2")
        contact = request.POST.get("t3")
        email = request.POST.get("t4")
        address = request.POST.get("t5")

        con = get_connection()
        cur = con.cursor()

        # Check whether username already exists
        cur.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        user = cur.fetchone()

        if user:
            cur.close()
            con.close()

            return render(
                request,
                "signup.html",
                {"msg": "Username already exists"}
            )

        # Insert new user
        cur.execute(
            """
            INSERT INTO users
            (username, password, contact, email, address)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (username, password, contact, email, address)
        )

        con.commit()

        cur.close()
        con.close()

        return render(
            request,
            "signup.html",
            {"msg": "Registration Successful"}
        )

    return render(request, "signup.html")

def login(request):
    if request.method == "POST":

        username = request.POST.get("t1")
        password = request.POST.get("t2")

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()

        cur.close()
        con.close()

        if user:
            return render(
                request,
                "home.html",
                {"username": username}
            )
        else:
            return render(
                request,
                "login.html",
                {"msg": "Invalid username or password"}
            )

    return render(request, "login.html")
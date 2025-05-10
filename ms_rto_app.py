from flask import Flask, request, render_template_string, session, redirect, url_for, send_file
from flask_session import Session
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Sample FAQ data
faq = {
    "mumbai-south": "Mumbai-South RTO Code is: MH01 and Office Address is: Tardeo RTO, Mumbai Central, Near Mumbai Central Railway Station, Mumbai-400008. Contact Number: 022-23078233 / 23078234",
    "mumbai-west": "Mumbai-West RTO Code is: MH02 and Office Address is: Andheri RTO, Andheri West, SV Road, Near Amboli Naka, Mumbai-400058. Contact Number: 022-26368214 / 26364657",
    "thane-east": "Thane-east RTO Code is: MH02 and Office Address is: Thane RTO, Near Thane Railway Station, Thane-400601. Contact Number: 022-25330091 / 25330092",
    "mumbai-east": "Mumbai-east RTO Code is: MH03 and Office Address is: Wadala RTO, Wadala Truck Terminal, Opposite Imax Theatre, Mumbai-400037. Contact Number: 022-24130091 / 24149657",
    "thane": "Thane RTO Code is: MH04 and Office Address is: Thane RTO, Eastern Express Highway, Near Cadbury Junction, Thane West-400601. Contact Number: 022-25475833",
    "kalyan": "Kalyan RTO Code is: MH05 and Office Address is: Kalyan RTO, Near Sai Baba Mandir, Haji Malang Road, Kalyan East, Maharashtra-421306. Contact Number: 0251-2364044",
    "raigad": "Raigad RTO Code is: MH06 and Office Address is: Raigad RTO, Mumbai-Goa Highway, Opposite RCF Plant, Alibag-402201. Contact Number: 02141-227398",
    "palghar": "Palghar RTO Code is: MH06 and Office Address is: Palghar RTO, Near Palghar Bus Stand, Palghar-401404. Contact Number: 02525-222508",
    "sindhudurg": "Sindhudurg RTO Code is: MH07 and Office Address is: Sindhudurg RTO, Sindhudurg Bhavan, Main Road, Kankavli-416602. Contact Number: 02367-232508",
    "ratnagiri": "Ratnagiri RTO Code is: MH08 and Office Address is: Ratnagiri RTO, Near Civil Hospital, Ratnagiri-415612. Contact Number: 02352-222220",
    "kolhapur": "Kolhapur RTO Code is: MH09 and Office Address is: Kolhapur RTO, PWD Building, Opposite Kolhapur Bus Stand, Kolhapur-416003. Contact Number: 0231-2658833",
    "sangli": "Sangli RTO Code is: MH10 and Office Address is: Sangli RTO, Near Miraj MIDC, Kupwad, Sangli-416436. Contact Number: 0233-2644747",
    "satara": "Satara RTO Code is: MH11 and Office Address is: Satara RTO, Civil Lines, Satara-415001. Contact Number: 02162-233508",
    "pune": "Pune RTO Code is: MH12 and Office Address is: Pune RTO, Near Sangam Bridge, Pune-411001. Contact Number: 020-26058080 / 26058090",
    "solapur": "Solapur RTO Code is: MH13 and Office Address is: Solapur RTO, Near Nila Nagar, Bijapur Road, Solapur-413005. Contact Number: 0217-2656601",
    "pimpri-chinchwad": "Pimpri-chinchwad RTO Code is: MH14 and Office Address is: Pimpri-Chinchwad RTO, Near Empire Estate, Old Pune-Mumbai Road, Chinchwad, Pune-411019. Contact Number: 020-27492828",
    "nashik": "Nashik RTO Code is: MH15 and Office Address is: Nashik RTO, Trimbak Road, Near Pandav Leni, Nashik-422007. Contact Number: 0253-2463304",
    "ahmednagar": "Ahmednagar RTO Code is: MH16 and Office Address is: Ahmednagar RTO, Near Zilla Parishad Office, Ahmednagar-414001. Contact Number: 0241-232508",
    "shrirampur": "Shrirampur RTO Code is: MH17 and Office Address is: Shrirampur RTO, Near Nagar Manmad Highway, Shrirampur, Maharashtra-413709. Contact Number: 02422-222418",
    "dhule": "Dhule RTO Code is: MH18 and Office Address is: Dhule RTO, Near MIDC, Shirpur Road, Dhule-424001. Contact Number: 02562-236507",
    "jalgaon": "Jalgaon RTO Code is: MH19 and Office Address is: Jalgaon RTO, NH-6, Near Maharashtra Engg. College, Jalgaon-425001. Contact Number: 0257-2263415",
    "akola": "Akola RTO Code is: MH20 and Office Address is: Akola RTO, Near Akola MIDC, Akola-444001. Contact Number: 0724-2433003",
    "aurangabad": "Aurangabad RTO Code is: MH20 and Office Address is: Regional Transport Office, Railway Station Rd, Rajnagar, MIDC, Chhatrapati Sambhaji Nagar, Maharashtra 431001. Contact Number: 0240‐2331135/2321164",
    "jalna": "Jalna RTO Code is: MH21 and Office Address is: Jalna RTO, Near Ghanshyam Theater, Mantha Road, Jalna-431203. Contact Number: 02482-234318",
    "parbhani": "Parbhani RTO Code is: MH22 and Office Address is: Parbhani RTO, Nanded Road, Parbhani-431401. Contact Number: 02452-233507",
    "beed": "Beed RTO Code is: MH23 and Office Address is: Beed RTO, Beed-Bhir Road, Beed-431122. Contact Number: 02442-232508",
    "latur": "Latur RTO Code is: MH24 and Office Address is: Latur RTO, Ring Road, Near Collector Office, Latur-413512. Contact Number: 02382-245673",
    "osmanabad": "Osmanabad RTO Code is: MH25 and Office Address is: Osmanabad RTO, NH-211, Near Bus Stand, Osmanabad-413501. Contact Number: 02472-223507",
    "nanded": "Nanded RTO Code is: MH26 and Office Address is: Marathwada Ceramic Complex, MIDC Cidco Nanded - 431603 Contact Number: 2462-259900",
    "amravati": "Amravati RTO Code is: MH27 and Office Address is: Amravati RTO, NH-6, Near Regional College, Amravati-444603. Contact Number: 0721-2552007",
    "buldhana": "Buldhana RTO Code is: MH28 and Office Address is: Buldhana RTO, Opposite Bus Stand, Khamgaon Road, Buldhana-443001. Contact Number: 07262-244208",
    "yavatmal": "Yavatmal RTO Code is: MH29 and Office Address is: Yavatmal RTO, Near Collector Office, Yavatmal-445001. Contact Number: 07232-243507",
    "nagpur": "Nagpur RTO Code is: MH31 and Office Address is: Nagpur RTO, Near University Campus, Nagpur-440010. Contact Number: 0712-2543222",
    "wardha": "Wardha RTO Code is: MH32 and Office Address is: Wardha RTO, Nagpur Road, Near PWD Office, Wardha-442001. Contact Number: 07152-233507",
    "gadchiroli": "Gadchiroli RTO Code is: MH33 and Office Address is: Gadchiroli RTO, Opposite Collector Office, Gadchiroli-442605. Contact Number: 07132-223300",
    "chandrapur": "Chandrapur RTO Code is: MH34 and Office Address is: Chandrapur RTO, Near Collectorate, Chandrapur-442402. Contact Number: 07172-274508",
    "gondia": "Gondia RTO Code is: MH35 and Office Address is: Gondia RTO, Near Gondia Bus Stand, Gondia-441601. Contact Number: 07182-251507",
    "bhandara": "Bhandara RTO Code is: MH36 and Office Address is: Bhandara RTO, Near Bus Stand, NH-6, Bhandara-441904. Contact Number: 07184-253507",
    "washim": "Washim RTO Code is: MH37 and Office Address is: Washim RTO, Near Bus Stand, NH-6, Washim-444505. Contact Number: 07252-234908",
    "hingoli": "Hingoli RTO Code is: MH38 and Office Address is: Hingoli RTO, Nanded Road, Near Hingoli Collectorate, Hingoli-431513. Contact Number: 02456-223308",
    "nandurbar": "Nandurbar RTO Code is: MH39 and Office Address is: Nandurbar RTO, Near Railway Station, Nandurbar-425412. Contact Number: 02564-223507",
    "nagpur-rural": "Nagpur Rural RTO Code is: MH40 and Office Address is: Nagpur Rural RTO, Near Nagpur University, Nagpur-440015. Contact Number: 0712-2547222",
    "malegaon": "Malegaon RTO Code is: MH41 and Office Address is: Malegaon RTO, NH-3, Near Municipal Corporation Office, Malegaon-423203. Contact Number: 02554-233408",
    "baramati": "Baramati RTO Code is: MH42 and Office Address is: Baramati RTO, Near Baramati MIDC, Baramati-413102. Contact Number: 02112-224508",
    "vashi": "Vashi, Navi Mumbai RTO Code is: MH43 and Office Address is: Vashi RTO, Near Vashi Railway Station, Navi Mumbai-400703. Contact Number: 022-27814667",
    "ambajogai": "Ambajogai RTO Code is: MH44 and Office Address is: Yeshwantrao Chavan Chowk, Morewadi, Ambajogai, Beed - 431517 Contact Number: 2446-247755",
    "akluj": "Akluj RTO Code is: MH45 and Office Address is: Rajhans Colony, Akluj, Maharashtra 413118 Contact Number: 2185-31231",
    "panvel, Khopoli": "Panvel, Khopoli RTO Code is: MH46 and Office Address is: Panvel RTO, Near Bus Stand, Khopoli-410206. Contact Number: 02192-263300",
    "borivali": "Borivali RTO Code is: MH47 and Office Address is: The Ambivali Village, New Manish Nagar, Versova Road, Mumbai - 400053 Contact Number: 22-26366957 / 26362252",
    "virar": "Virar RTO Code is: MH48 and Office Address is: Mu Po, Chandansar Rd, Bhatpada, Chandansar, Virar, Maharashtra 401303 Contact Number: 250-2523888",
    "nagpur-east": "Nagpur East RTO Code is: MH49 and Office Address is: Nagpur East RTO, Near Bhandewadi, Nagpur-440009. Contact Number: 0712-272222",
    "karad": "Karad RTO Code is: MH50 and Office Address is: Karad RTO, NH-4, Near Bus Stand, Karad-415110. Contact Number: 02164-223200",
    "nashik-rural": "Nashik Rural RTO Code is: MH51 and Office Address is: Nashik Rural RTO, Near Wani Phata, Nashik-422209. Contact Number: 0253-2462310",
    "parbhani-rural": "Parbhani Rural RTO Code is: MH52 and Office Address is: Parbhani Rural RTO, Near Parbhani Bus Stand, Parbhani-431405. Contact Number: 02452-245007",
    "pune-south": "Pune-South RTO Code is: MH53 and Office Address is: Pune South RTO, Satara Road, Pune-411009. Contact Number: 020-24216222",
    "pune-north": "Pune-North RTO Code is: MH54 and Office Address is: Pune North RTO, Near Nashik Phata, Pune-411019. Contact Number: 020-27492888",
    "mumbai-central": "Mumbai Central RTO Code is: MH55 and Office Address is: Mumbai Central RTO, Mumbai Central, Near Mumbai Central Railway Station, Mumbai-400008. Contact Number: 022-23072838",
}

# HTML template
html_template = """
<!doctype html>
<html>
<style>
    body {
        background-color: #D3D3D3; /* Light gery scrren background */
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
</style>

<head>
    <title>Maharashtra State RTO Info Chatbot</title>
</head>
<body>
<h2 style="text-align:center;">Maharashtra State RTO Code & Address Information ChatBot</h2>
        <form method="post" action="/">
        <input name="message" placeholder="Enter Maharashtra state City/District/Town name..." style="width:600px;" required>
        <input type="submit" value="Find">
    </form>
   
     <br>  <!-- Adds two blank lines -->

    <form method="post" action="/clear" style="display:inline;">
        <input type="submit" value="Clear Summary">
    </form>

    <form method="post" action="/create_pdf" style="display:inline;">
        <input type="submit" value="Create Summary PDF File">
    </form>

    {% if user_message %}
        <p><strong>You:</strong> {{ user_message }}</p>
        <p><strong>Bot:</strong> {{ response }}</p>
    {% endif %}

    {% if history %}
        <hr>
        <h3>Chat Summary:</h3>
        <ul>
        {% for msg, reply in history %}
            <li><strong>You:</strong> {{ msg }}<br><strong>Bot:</strong> {{ reply }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if 'history' not in session:
        session['history'] = []

    user_message = ""
    response = ""

    if request.method == "POST":
        user_message = request.form["message"]
        message_lower = user_message.lower()
        response = "Sorry! This City/District/Town has no RTO office, please try another!"

        for question in faq:
            if question.lower() in message_lower:
                response = faq[question]
                break

        history = session['history']
        history.append((user_message, response))
        session['history'] = history

    return render_template_string(
        html_template,
        user_message=user_message,
        response=response,
        history=session.get('history', [])
    )

@app.route("/clear", methods=["POST"])
def clear_summary():
    session.pop('history', None)
    return redirect(url_for('chatbot'))

@app.route("/create_pdf", methods=["POST"])
def create_pdf():
    history = session.get('history', [])

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)

    y = 800
    for idx, (msg, reply) in enumerate(history):
        p.drawString(50, y, f"You: {msg}")
        y -= 20
        p.drawString(50, y, f"Bot: {reply}")
        y -= 30
        if y < 100:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 800

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="chat_summary.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)

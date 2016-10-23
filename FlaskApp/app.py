from flask import Flask, render_template
app=Flask(__name__)

mylocation = []
mylocation.append(40.741895)
mylocation.append(-73.989308)

@app.route("/")
def main():
	return render_template('index.html',context=mylocation)



if __name__ == "__main__":
	app.run(port=8000,debug=True)
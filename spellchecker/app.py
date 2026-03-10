"""Main file for handling trie"""
import traceback
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash

from src.trie import Trie
from src.error import SearchMiss


app = Flask(__name__)
app.secret_key = re.sub(r"[^a-z\d]", "", os.path.realpath(__file__))


@app.route("/")
def main():
    """Main route. """
    return redirect(url_for('init'))

@app.route("/init")
def init():
    """
    The init file.
    """
    if "file" not in session:
        session["file"] = "./frequency.txt"
    if "remove" not in session:
        session["remove"] = ""
    if "search-prefix" not in session:
        session["search-prefix"] = ""
    if "word_found" not in session:
        session["word_found"] = None
    if "prefix_found" not in session:
        session["prefix_found"] = []
    if "suffix_found" not in session:
        session["suffix_found"] = []
    if "search_suffix" not in session:
        session["search_suffix"] = ""
    if "remove_word" not in session:
        session["remove_word"] = []
    return render_template("home.html")


@app.route("/check-word", methods=["GET"])
def check_word():
    """GET route for checking a word """

    return render_template("check.html", word_found=session["word_found"])

@app.route("/check-word", methods=["POST"])
def check_word_post():
    """POST route for checking a word """
    search = request.form.get("check-word").strip()

    trie = Trie()
    file = session.get("file")
    trie.open_file(file)
    try:
        if "remove_word" in session:
            removed_list = session.get("remove_word", [])
            for word in removed_list:
                trie.remove(word)
        result = trie.search(search)

    except SearchMiss:
        result = False

    session["word_found"] = result

    if result:
        flash(f"The word {search} is spelled correctly!", "success")
    else:
        flash(f"The word {search} is NOT spelled correctly!", "danger")

    return redirect(url_for("check_word"))

@app.route("/prefix", methods=["GET"])
def prefix():
    """GET route for checking a word """

    return render_template("prefix.html",
    prefix_found=session["prefix_found"],
    search_prefix=session["search-prefix"])

@app.route("/prefix", methods=["POST"])
def prefix_post():
    """POST route for checking a word """
    search = request.form.get("prefix").strip()

    trie = Trie()
    file = session.get("file")
    trie.open_file(file)
    try:
        if "remove_word" in session:
            removed_list = session.get("remove_word", [])
            for word in removed_list:
                trie.remove(word)
        result = trie.prefix_search(search)

    except SearchMiss:
        result = False
    print(result)
    session["prefix_found"] = result
    session["search-prefix"] = search

    if result:
        pass
    else:
        flash(f"There is no word starting with {search}", "danger")

    return redirect(url_for("prefix"))

@app.route("/suffix", methods=["GET"])
def suffix():
    """GET route for checking a word """

    return render_template("suffix.html",
    suffix_found=session["suffix_found"],
    search_suffix=session["search_suffix"])

@app.route("/suffix", methods=["POST"])
def suffix_post():
    """POST route for checking a word """
    search = request.form.get("suffix").strip()

    trie = Trie()
    file = session.get("file")
    trie.open_file(file)
    try:
        if "remove_word" in session:
            removed_list = session.get("remove_word", [])
            for word in removed_list:
                trie.remove(word)
        result = trie.suffix_search(search)

    except SearchMiss:
        result = False
    print(result)
    session["suffix_found"] = result
    session["search_suffix"] = search

    if result:
        pass
    else:
        flash(f"There is no word ending with {search}", "danger")

    return redirect(url_for("suffix"))

@app.route("/remove-word", methods=["GET"])
def remove_word():
    """GET route for removing a word """

    return render_template("remove.html", remove_word=session["remove_word"])

@app.route("/remove-word", methods=["POST"])
def remove_word_post():
    """POST route for removing a word """
    removed = request.form.get("remove-word").strip()

    removed_list = session.get("remove_word", [])
    trie = Trie()
    file = session.get("file")
    trie.open_file(file)

    try:
        result = trie.search(removed)
    except SearchMiss:
        result = False

    session["word_found"] = result

    if result:
        flash(f"The word {removed} is removed from the dictionary", "success")
        removed_list.append(removed)
        session["remove_word"] = removed_list
    else:
        flash(f"The word {removed} does not exist and cannot be removed","danger")

    return redirect(url_for("remove_word"))

@app.route("/show-all")
def show_all():
    """ Route for showing all words """
    trie = Trie()
    file = session.get("file")
    trie.open_file(file)
    try:
        if "remove_word" in session:
            removed_list = session.get("remove_word", [])
            for word in removed_list:
                trie.remove(word)
    except SearchMiss:
        pass
    amount = trie.count()
    all_words = trie.all_words()
    all_sorted = sorted(all_words)
    return render_template("show-all.html", all_sorted=all_sorted, amount=amount)

@app.route("/change-file", methods=["GET"])
def change_file():
    """ GET route for changing file """
    files = ["./frequency.txt", "./tiny_frequency.txt"]
    current_file = session.get("file")
    files.remove(current_file)
    return render_template("change-file.html", files=files, current_file=current_file)

@app.route("/change-file", methods=["POST"])
def change_file_post():
    """ POST route for changing file """
    selected_file = request.form.get("file")
    print(f"Selected file: {selected_file}")
    session["file"] = selected_file
    session["remove_word"] = []
    return redirect(url_for("change_file"))

@app.route("/reset")
def reset():
    """ Route for reset session """
    _ = [session.pop(key) for key in list(session.keys())]
    # Det var denna kod Andreas använde under föreläsningen men här är en for-loop ändå.
    # for key in list(session.keys()):
    # session.pop(key)
    return redirect(url_for('main'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."



@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument
    return "<p>Flask 500<pre>" + traceback.format_exc()


if __name__ == "__main__":
    app.run(debug=True)

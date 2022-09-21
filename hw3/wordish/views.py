from django.shortcuts import render

# Create your views here.

def start_action(request):
    if request.method == "GET":
        context = {"message": "Welcome to Wordish"}
        context["game_page"] = "start"
        return render(request, "wordish/startpage.html", context)
    try:
        target = _process_param(request.POST, "target")
        context = _compute_context(target, guesses=[])
        context["game_page"] = "guess"
        return render(request, "wordish/wordish.html", context)
    except Exception as e:
        context = {"message": "invalid input: " + str(e)}
        context["game_page"] = "start"
        return render(request, "wordish/startpage.html", context)

def guess_action(request):
    if request.method == "GET":
        context = {"message": "You're hacking. Try again!"}
        return render(request, "wordish/startpage.html", context)

    try:
        target = _process_param(request.POST, "target")
        old_guesses = _process_old_guesses(request.POST)
    except Exception as e:
        context = {"message": f"Fatal error: {e}"}
        context["game_page"] = "start"
        return render(request, "wordish/startpage.html", context)

    try:
        new_guess = _process_param(request.POST, "new-guess")
        context = _compute_context(target, old_guesses + [new_guess])
    except Exception as e:
        print(f"exception is: {str(e)}")
        context = _compute_context(target, old_guesses)
        # context["game_page"] = "start"
        context["status"] = f"Invalid input: {e}"
    context["game_page"] = "guess"
    return render(request, "wordish/wordish.html", context)

def _process_old_guesses(post):
    if post["guesses"] == "":
        return []
    guess_list = post["guesses"].split(",")
    for word in guess_list:
        if len(word) != 5:
            raise Exception("invalid input")
        for letter in word:
            if ord(letter) < ord('a') or ord(letter) > ord('z'):
                raise Exception("invalid input")
    return guess_list

def get_color(target, word, color_list):
    win = False
    if target == word:
        win = True
    for i in range(5):
        x, y = word[i], target[i]
        color_list[i] = "gray"
        if x == y:
            color_list[i] = "green"
            target = target[:i] + "_" + target[i + 1:]
    
    for i in range(5):
        x = word[i]
        idx = target.find(x)
        if (idx != -1) and color_list[i] != "green":
            color_list[i] = "yellow"
            target = target[:idx] + "_" + target[idx + 1:]
    return win
        

def _compute_context(target, guesses):
    matrix = {}
    win = False
    for row in range(6):
        matrix[row] = {}
        for col in range(5):
            matrix[row][col] = {"id": f"cell_{row}_{col}", "letter": "", \
                    "color": "white"}
    for row in range(6):
        color_list = ["white"] * 5
        if row < len(guesses):
            win = get_color(target, guesses[row], color_list)
        for col in range(5):
            letter = ""
            if row < len(guesses):
                letter = guesses[row][col]
            cell = {"id": f"cell_{row}_{col}", "letter": f"{letter}", \
                    "color": f"{color_list[col]}"}
            matrix[row][col] = cell
        if win:
            break
    if len(guesses) == 0:
        status = "start"
    elif len(guesses) < 6 and not win:
        status = "playing"
    elif win:
        status = "win"
    else:
        status = "lose"
    guesses = ",".join(guesses)
    context = {
        "status": status,
        "matrix": matrix,
        "target": target,
        "guesses": guesses
    }
    return context

def _process_param(post, name):
    if name not in post:
        raise Exception("name not in post")
    else:
        target = post[name]
        if len(target) != 5:
            raise Exception("word length less than 5")
        for letter in target:
            if ord(letter) < ord('a') or ord(letter) > ord('z'):
                raise Exception("invalid character")
        return post[name]
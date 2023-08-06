# Coldfilms

A python API for icefilms

# TODO

    secret = soup.find("input", name="secret")["value"]

    # OR

    for script in soup("script"):
        m = re.search(r'f.lastChild.value=("[^"]+"),', script.text)
        if not m:
            continue
        secret = json.loads(m.group(1))
        break

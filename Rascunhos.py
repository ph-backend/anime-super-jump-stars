while jotaro.life > 0 and dio.life > 0:
    show_status(jotaro, dio)
    show_skills(jotaro)
    choice = input("Choose skill (0 for basic): ")
    if choice == "3":
        jotaro.attack(dio)
    else:
        idx = int(choice) - 1
        jotaro.skills[idx].use(jotaro, dio) # Inimigo automático
    if dio.life > 0: dio.attack(jotaro)
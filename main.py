from db import connect_db
from service import (
    list_subdivisions,
    list_links,
    run_analysis,
    add_subdivision,
    edit_subdivision,
    delete_subdivision,
    add_link,
    delete_link,
    edit_link,
)


def main_menu(db_path: str = "company.db", company_id: int = 1) -> None:
    conn = connect_db(db_path)

    while True:
        print("============== МЕНЮ СИСТЕМЫ ==============")
        print("1. Показать подразделения")
        print("2. Показать связи")
        print("3. Запустить анализ компании")
        print("4. Добавить подразделение")
        print("5. Изменить подразделение")
        print("6. Удалить подразделение")
        print("7. Добавить связь")
        print("8. Удалить связь")
        print("9. Изменить связь")
        print("0. Выход")
        choice = input("Ваш выбор: ").strip()
        print()

        if choice == "1":
            list_subdivisions(conn, company_id)
        elif choice == "2":
            list_links(conn, company_id)
        elif choice == "3":
            run_analysis(conn, company_id)
        elif choice == "4":
            add_subdivision(conn, company_id)
        elif choice == "5":
            edit_subdivision(conn, company_id)
        elif choice == "6":
            delete_subdivision(conn, company_id)
        elif choice == "7":
            add_link(conn, company_id)
        elif choice == "8":
            delete_link(conn, company_id)
        elif choice == "9":
            edit_link(conn, company_id)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда.\n")

    conn.close()


if __name__ == "__main__":
    main_menu()

# Задание:
# https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping


from ArticleExtractor import get_articles


STARL_URL = 'https://habr.com/ru/all/'

KEYWORDS = ('python', 'дизайн', 'фото')


if __name__ == "__main__":

    print(
        f'''Поиск статей
        Начальный адрес:  {STARL_URL} 
        Ключевые слова:   {', '.join(KEYWORDS)}'''
    )

    results = get_articles(STARL_URL, KEYWORDS)
    for result in results:
        print('\n', result[0], '-', result[1], '-', result[2])

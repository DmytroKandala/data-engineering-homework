/*
Завдання на SQL до лекції 03.
*/

/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT
    c.name AS category_name,
    COUNT(f.film_id) AS film_count
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
GROUP BY c.name
ORDER BY film_count DESC;

/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
SELECT
    a.first_name || ' ' || a.last_name AS actor_name,
    COUNT(r.rental_id) AS rental_count
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN inventory i ON fa.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY actor_name
ORDER BY rental_count DESC
LIMIT 10;

/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
SELECT
    c.name AS category_name,
    SUM(p.amount) AS total_revenue
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY c.name
ORDER BY total_revenue DESC
LIMIT 1;

/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT f.title
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
WHERE i.film_id IS NULL;

/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
SELECT
    a.first_name || ' ' || a.last_name AS actor_name,
    COUNT(*) AS film_count
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
WHERE c.name = 'Children'
GROUP BY actor_name
ORDER BY film_count DESC
LIMIT 3;

/*
Додатково
Вивести топ-5 акторів із найбільшою сумарною тривалістю фільмів (у годинах і хвилинах), у яких вони знімались.
*/
SELECT
    a.first_name || ' ' || a.last_name AS actor_name,
    SUM(f.length) AS total_minutes,
    FLOOR(SUM(f.length) / 60) || 'h ' || MOD(SUM(f.length), 60) || 'm' AS total_duration
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN film f ON fa.film_id = f.film_id
GROUP BY actor_name
ORDER BY total_minutes DESC
LIMIT 5;

/*
Вивести топ-5 акторів, фільми яких найчастіше брали в оренду.
*/
SELECT
    a.first_name || ' ' || a.last_name AS actor_name,
    COUNT(r.rental_id) AS rental_count
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN inventory i ON fa.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY actor_name
ORDER BY rental_count DESC
LIMIT 5;

/*
Вивести топ-5 фільмів, що принесли найбільшу виручку з оренди.
*/
SELECT
    f.title,
    SUM(p.amount) AS total_revenue
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY f.title
ORDER BY total_revenue DESC
LIMIT 5;

/*
Вивести кількість оренд за останні 30 днів.
*/
SELECT
    COUNT(*) AS rental_count_last_30_days
FROM rental;

/*
Вивести суми виручки та кількість прокатів по роках.
*/
SELECT
    EXTRACT(YEAR FROM payment_date) AS year,
    COUNT(*) AS rental_count,
    SUM(amount) AS total_revenue
FROM payment
GROUP BY year
ORDER BY year;

/*
Оскільки всі продажі здійснювались лише протягом одного року, вивести мінімальну та максимальну дату здійснення оплати.
*/
SELECT
    MIN(payment_date) AS min_date,
    MAX(payment_date) AS max_date
FROM payment;

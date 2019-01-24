use sakila;

-- 1a. Display the first and last names of all actors from the table actor.
select distinct first_name, last_name from actor order by last_name;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
select concat(upper(first_name), " ", upper(last_name)) as `Actor Name` from actor order by 1;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
select * from actor where first_name like '%joe%';

-- 2b. Find all actors whose last name contain the letters GEN:
select * from actor where last_name like '%gen%';

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
select * from actor where last_name like '%li%' order by last_name, first_name;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
select country_id, country from country where country in ('Afghanistan', 'Bangladesh', 'China');

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
alter table actor add column description BLOB;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
alter table actor drop column description;

-- 4a. List the last names of actors, as well as how many actors have that last name.
select last_name, count(*) from actor group by last_name order by count(*) desc;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
select last_name, count(*) from actor group by last_name having count(*)>1 order by count(*) desc;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
update actor set first_name='HARPO' where first_name ='GROUCHO' and last_name='WILLIAMS';

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
update actor set first_name='GROUCHO' where first_name ='HARPO' and last_name='WILLIAMS';

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
show create table address;

CREATE TABLE `address` (
   `address_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
   `address` varchar(50) NOT NULL,
   `address2` varchar(50) DEFAULT NULL,
   `district` varchar(20) NOT NULL,
   `city_id` smallint(5) unsigned NOT NULL,
   `postal_code` varchar(10) DEFAULT NULL,
   `phone` varchar(20) NOT NULL,
   `location` geometry NOT NULL,
   `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`address_id`),
   KEY `idx_fk_city_id` (`city_id`),
   SPATIAL KEY `idx_location` (`location`),
   CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON UPDATE CASCADE
 ) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8;
 
-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
select x.first_name, x.last_name, y.address
from staff x
left join address y  on x.address_id=y.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
select x.first_name, x.last_name, sum(amount)
from staff x
left join payment y on x.staff_id=y.staff_id
where payment_date between '2005-08-01' and '2005-08-31'
group by x.first_name, x.last_name;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
select x.title, count(*) as actor_count
from film x
inner join film_actor y on x.film_id=y.film_id
group by x.title;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
select count(*)
from inventory x
left join film y on x.film_id=y.film_id
where y.title='Hunchback Impossible';

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
select x.first_name, x.last_name, sum(y.amount)
from customer x
left join payment y on x.customer_id=y.customer_id
group by x.first_name, x.last_name
order by x.last_name;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
select x.*
from film x
inner join (select name, language_id from language where name='English') y on x.language_id=y.language_id
where x.title like 'Q%' or x.title like 'K%';

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
select x.*
from actor x
inner join film_actor y on x.actor_id=y.actor_id
inner join (select title, film_id from film where title='Alone Trip') z on y.film_id=z.film_id;

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
select a.first_name, a.last_name, a.email
from customer a
inner join address b on a.address_id=b.address_id
inner join city c on b.city_id=c.city_id
inner join (select country_id, country from country where country='Canada') d on c.country_id=d.country_id;

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
select x.*
from film x
inner join film_category y on x.film_id=y.film_id
inner join (select category_id, name from category where name='Family') z on y.category_id=z.category_id;
-- there are an uncomfortable number of NC-17 "Family" films

-- 7e. Display the most frequently rented movies in descending order.
select a.title, count(*)
from film a
inner join inventory b on a.film_id = b.film_id
inner join rental c on b.inventory_id = c.inventory_id
group by a.title
order by count(*) desc;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
select a.store_id, sum(c.amount)
from store a
inner join customer b on a.store_id = b.store_id
inner join payment c on  b.customer_id = c.customer_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
select a.store_id, c.city, d.country
from store a
inner join address b on a.address_id = b.address_id
inner join city c on b.city_id = c.city_id
inner join country d on c.country_id=d.country_id;

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following 
-- tables: category, film_category, inventory, payment, and rental.)
select c.name, sum(p.amount)
from payment p
join rental r on p.rental_id=r.rental_id
join inventory i on r.inventory_id=i.inventory_id
join film_category fc on i.film_id=fc.film_id
join category c on fc.category_id=c.category_id
group by c.name
order by sum(p.amount) desc
limit 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres 
-- by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, 
-- you can substitute another query to create a view.
create view top_five_genres as
select c.name as genre, sum(p.amount) as gross_revenue
from payment p
join rental r on p.rental_id=r.rental_id
join inventory i on r.inventory_id=i.inventory_id
join film_category fc on i.film_id=fc.film_id
join category c on fc.category_id=c.category_id
group by c.name
order by sum(p.amount) desc
limit 5;

-- 8b. How would you display the view that you created in 8a?
select * from top_five_genres;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
drop view if exists top_five_genres;

/*1.  Ver todos los nombres y distritos de las ciudades */;
CREATE VIEW Vista_01 AS 
SELECT Name, District FROM city;

/*2.  Ver todas las ciudades que tienen el código ESP */;
CREATE VIEW Vista_02 AS 
SELECT * FROM city WHERE countrycode LIKE 'ESP';

/*3.  Ver todas las ciudades y sus códigos de pais, ordenados por código de país */;
CREATE VIEW Vista_03 AS 
SELECT Name, countrycode FROM city ORDER BY countrycode;

/*4.  Sacar la población menor,mayor,y la medía. */;
CREATE VIEW Vista_04 AS 
SELECT 
    min(population) AS 'Menor población', 
    max(population) AS 'Mayor población', 
    avg(population) AS 'Media de población'
FROM city ORDER BY countrycode;

/*5.  Sacar el nombre de la ciudad con más habitantes */;
CREATE VIEW Vista_05 AS 
SELECT Name AS 'Ciudad con más habitantes' FROM city
WHERE population = (SELECT max(population) FROM city);

/*6.  Ver todas las Provincias(distritos) de España */;
CREATE VIEW Vista_06 AS 
SELECT distinct district FROM city 
WHERE countrycode = (
    SELECT code FROM country 
    WHERE Name like 'Spain'
    );

/*7.  Ver el número de ciudades por provincia de España */;
CREATE VIEW Vista_07 AS 
select district, count(*) AS 'número de ciudades' 
from city 
where countrycode like 'ESP%' 
group by district;

/*8.  Ver todas las ciudades de Madrid */;
CREATE VIEW Vista_08 AS 
SELECT Name FROM city 
WHERE district = 'Madrid';

/*9.  Ver la Lista de capitales africanas */;
CREATE VIEW Vista_09 AS 
SELECT 
    country.Name AS 'nombre de la ciudad', 
    city.Name AS 'nombre de la capital'
FROM country
LEFT JOIN city ON country.Capital = city.ID
WHERE country.Continent = 'Africa';

/*10. Sacar los países, con su esperanza de vida. */;
CREATE VIEW Vista_10 AS 
SELECT 
    Name, 
    LifeExpectancy AS 'Esperanza de vida' 
FROM country;

/*11. Obtén una lista con los siguientes campos: Ciudad, poblacion, país, superficie, idioma oficial. */;
CREATE VIEW Vista_11 AS
SELECT 
    city.Name AS Ciudad,
    city.Population AS 'Poblacion urbana',
    country.Name AS Pais,
    country.SurfaceArea AS 'Superficie pais',
    country.Population AS 'Poblacion total_pais',
    countrylanguage.Language AS 'Idioma Oficial'
FROM country 
INNER JOIN city ON country.code = city.countrycode 
INNER JOIN countrylanguage ON country.code = countrylanguage.countrycode
WHERE countrylanguage.IsOfficial = 'T';

/*12. Obtén el nombre de la capital de todos los países. */;
CREATE VIEW Vista_12 AS 
SELECT country.Name AS País, 
    IFNULL(city.Name, 'Sin capital') AS Capital
FROM country
LEFT JOIN city ON country.Capital = city.ID;

/*13. Lista todos los países con más de 1 millón de habitantes con sus capitales y la lengua oficial */;
CREATE VIEW Vista_13 AS 
SELECT 
    country.Name AS País,
    city.Name AS Capital,
    countrylanguage.Language AS 'Lengua Oficial'
FROM country
INNER JOIN city ON country.Capital = city.ID
INNER JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
WHERE country.Population > 1000000
AND countrylanguage.IsOfficial = 'T';

/*14. Cuantos idiomas tiene cada país. */;
CREATE VIEW Vista_14 AS 
SELECT 
    country.Name AS País,
    COUNT(countrylanguage.Language) AS 'Número de idiomas'
FROM country
LEFT JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
GROUP BY country.Name;

/*15. Saca el jefe de gobierno de cada país */;
CREATE VIEW Vista_15 AS 
SELECT 
    country.Name AS País,
    country.HeadOfState AS 'Jefe de gobierno'
FROM country;



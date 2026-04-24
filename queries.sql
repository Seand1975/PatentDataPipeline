-- Q1: Who has the most patents? (Top organization IDs)
SELECT gi_organization_id, COUNT(*) AS patent_count
FROM patents_orgs
GROUP BY gi_organization_id
ORDER BY patent_count DESC
LIMIT 10;


-- Q2: Top Organizations (by agency name)
SELECT fedagency_name, COUNT(*) AS patent_count
FROM patents_orgs
GROUP BY fedagency_name
ORDER BY patent_count DESC
LIMIT 10;


-- Q3: Countries producing the most patents
SELECT foreign_country_filed, COUNT(*) AS patent_count
FROM patents_priority
GROUP BY foreign_country_filed
ORDER BY patent_count DESC
LIMIT 10;


-- Q4: Trends Over Time (patents per year)
SELECT 
    EXTRACT(YEAR FROM filing_date) AS year,
    COUNT(*) AS patent_count
FROM patents_priority
WHERE filing_date IS NOT NULL
GROUP BY year
ORDER BY year;


-- Q5: JOIN Query (combine orgs + priority data)
SELECT 
    p.patent_id,
    p.gi_organization_id,
    p.fedagency_name,
    pr.foreign_country_filed,
    pr.filing_date
FROM patents_orgs p
JOIN patents_priority pr
ON p.patent_id = pr.patent_id
LIMIT 20;


-- Q6: CTE Query (step-by-step breakdown)
WITH patent_counts AS (
    SELECT 
        gi_organization_id,
        COUNT(*) AS total_patents
    FROM patents_orgs
    GROUP BY gi_organization_id
),
top_orgs AS (
    SELECT *
    FROM patent_counts
    WHERE total_patents > 5
)
SELECT *
FROM top_orgs
ORDER BY total_patents DESC;


-- Q7: Ranking Query (window function)
SELECT 
    gi_organization_id,
    COUNT(*) AS patent_count,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
FROM patents_orgs
GROUP BY gi_organization_id;
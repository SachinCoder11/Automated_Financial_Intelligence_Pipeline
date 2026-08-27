create database Finance_EDA;
use Finance_eda;

USE finance_eda;

RENAME TABLE `company_master_data_2026-08-25 (1)`
TO company_master;

DESCRIBE company_master;

SELECT
    CIN,
    `Company Name`,
    `Company Address`,
    `Pin Code`,
    `Company State`
FROM company_master
LIMIT 20;

SELECT COUNT(*) AS total_companies
FROM company_master;


SELECT COUNT(DISTINCT CIN) AS unique_cins
FROM company_master;

SELECT *
FROM company_master
WHERE CONCAT_WS(
    ' ',
    CIN,
    `Company Name`,
    `Company Address`,
    `Pin Code`,
    `Company State`,
    `Company Status`,
    `Company Sub Category`,
    `Company Industrial Classification`,
    `Company ROC`,
    `Company Category`,
    `Company Class`,
    `Listing Status`
) LIKE '%C-5704502C%';

SELECT *
FROM company_master
WHERE CONCAT_WS(
    ' ',
    CIN,
    `Company Name`,
    `Company Address`,
    `Pin Code`,
    `Company State`,
    `Company Status`,
    `Company Sub Category`,
    `Company Industrial Classification`,
    `Company ROC`,
    `Company Category`,
    `Company Class`,
    `Listing Status`
) LIKE '%C-5704502C%';
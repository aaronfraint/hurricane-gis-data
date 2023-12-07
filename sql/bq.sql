create or replace table
  hackathon_workflows_2023.all_years_pgn_timestamp as

with verbose_date as (
  SELECT
  cast(SPLIT(ADVDATE, ' ')[ordinal(1)] as integer)/100 as hr,
  SPLIT(ADVDATE, ' ')[ordinal(2)] as ampm,
  SPLIT(ADVDATE, ' ')[ordinal(3)] as tz,
  SPLIT(ADVDATE, ' ')[ordinal(5)] as month,
  SPLIT(ADVDATE, ' ')[ordinal(6)] as day,
  SPLIT(ADVDATE, ' ')[ordinal(7)] as year, ADVDATE, geom, stormname, stormtype
FROM `cartodb-gcp-solutions-eng-team.hackathon_workflows_2023.all_years_pgn`
where advdate not like '%/%'
),
slash_date as (
  SELECT
    ADVDATE,
    substr(ADVDATE, 0, 2) as year,  
    substr(ADVDATE, 3, 2) as month,  
    substr(ADVDATE, 5, 2) as day,  
    substr(ADVDATE, 8, 2) as hr,  
    geom,
    stormname, stormtype, 
  FROM `cartodb-gcp-solutions-eng-team.hackathon_workflows_2023.all_years_pgn`
  where advdate  like '%/%' and length(advdate) = 11
),
converted as (
  select
    PARSE_DATETIME(
    '%b %d %Y %I %p',
    concat(month, ' ', day, ' ', year, ' ', round(hr), ' ', ampm)
    ) as dt, geom, stormname, stormtype, 
  from verbose_date

  union all

  select
    parse_datetime(
      '%Y-%m-%d %H',
      concat(20, year, '-', month, '-', day, ' ', hr)
    ) as dt, geom, stormname, stormtype
    from slash_date

)

select *
from converted order by dt

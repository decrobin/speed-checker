CREATE TABLE speed_results (
    id             serial           primary key,
    date           VARCHAR(20)      not null,
    time           VARCHAR(20)      not null,
    ping           VARCHAR(20)      not null,
    download       VARCHAR(20)      not null,
    upload         VARCHAR(20)      not null
);
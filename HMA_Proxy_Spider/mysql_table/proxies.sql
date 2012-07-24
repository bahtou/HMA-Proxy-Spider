CREATE TABLE Proxies (
    IPID            int NOT NULL AUTO_INCREMENT,
    IP_Address      varchar(15),
    Port            mediumint,
    loadTime        bigint,
    lastUpdate      int,
    Country         varchar(35),
    speedValue      smallint,
    speedDesc       varchar(6),
    connTimeValue   smallint,
    connTimeDesc    varchar(6),
    proxyType       varchar(8),
    Anonymity       varchar(8),
    PRIMARY KEY(IPID, loadTime)
    ) ENGINE = InnoDB;

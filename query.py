query = """INSERT INTO cases (
    countryother,
    totalcases,
    newcases,
    totaldeaths,
    newdeaths,
    totalrecovered,
    activecases,
    seriouscritical,
    totcases1mpop,
    deaths1mpop,
    firstcase) VALUES 
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (countryother)
    DO UPDATE SET
    totalcases=e.totalcases,
    newcases=e.newcases,
    totaldeaths=e.totaldeaths,
    newdeaths=e.newdeaths,
    totalrecovered=e.totalrecovered,
    activecases=e.activecases,
    seriouscritical=e.seriouscritical,
    totcases1mpop=e.totcases1mpop,
    deaths1mpop=e.deaths1mpop
    FROM 
    (VALUES %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
    as e(
        countryother,
        totalcases,
        newcases,
        totaldeaths,
        newdeaths,
        totalrecovered,
        activecases,
        seriouscritical,
        totcases1mpop,
        deaths1mpop,
        firstcase
    )
    WHERE countryother=e.countryother;
    """
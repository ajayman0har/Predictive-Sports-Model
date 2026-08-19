#this file converts american moneyline to probability, removes vig, and calculates the payout from a bet with the determined moneyline

def moneyline_to_odds(moneyline):
    odds = 0
    if moneyline > 0:
        odds = 100/(moneyline + 100)
    elif moneyline < 0:
        odds = abs(moneyline)/(abs(moneyline)+100)
    else:
        raise ValueError("Moneyline not valid")

    return odds


def find_fair_prob(home_raw_prob,away_raw_prob):
    total = home_raw_prob + away_raw_prob
    home_fair_prob = home_raw_prob/total
    away_fair_prob = away_raw_prob/total
    return home_fair_prob, away_fair_prob

def moneyline_to_payout(moneyline, wager):
    if moneyline > 0:
        return moneyline/100 * wager
    elif moneyline < 0:
        return 100/abs(moneyline) * wager
    else :
        raise ValueError("Moneyline not valid")
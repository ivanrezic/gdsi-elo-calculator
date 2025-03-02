def get_probs_pre(player1_elo, player2_elo):
    k = (player2_elo - player1_elo) / 400.0;
    player1_prob_pre = 1.0 / (1.0 + 10 ** k);
    return player1_prob_pre, 1 - player1_prob_pre


def get_probs_post(match_result):
    sets_num = len(match_result)

    gems_num = 0
    for s in match_result:
        gems_num += s[0] + s[1]

    prob_post = 0.5
    if sets_num == 3:
        prob_post = 0.5
    elif gems_num < 13:
        prob_post = 1
    elif gems_num < 14:
        prob_post = 0.95
    elif gems_num < 15:
        prob_post = 0.9
    elif gems_num < 17:
        prob_post = 0.85
    elif gems_num < 19:
        prob_post = 0.8
    elif gems_num < 21:
        prob_post = 0.75
    elif gems_num < 23:
        prob_post = 0.7
    elif gems_num < 25:
        prob_post = 0.6
    elif gems_num < 27:
        prob_post = 0.55

    player1_prob_post = prob_post
    player2_prob_post = 1 - player1_prob_post

    return player1_prob_post, player2_prob_post


def calc_elos(player1_elo, player1_match_num,
              player2_elo, player2_match_num,
              match_result):
    ####### added to ignore position of winning player
    second_won = False
    player_1_points = 0
    player_2_points = 0

    for s in match_result:
        player_1_points += s[0]
        player_2_points += s[1]

    second_won = player_2_points > player_1_points

    if second_won:
        player1_elo, player2_elo = player2_elo, player1_elo
        player1_match_num, player2_match_num = player2_match_num, player1_match_num
    #######

    probs_pre = get_probs_pre(player1_elo, player2_elo)
    probs_post = get_probs_post(match_result)

    player1_prob_pre = probs_pre[0]
    player2_prob_pre = probs_pre[1]
    player1_prob_post = probs_post[0]
    player2_prob_post = probs_post[1]

    player1_K = max(50.0, 300 - player1_match_num * 2.5)
    player2_K = max(50.0, 300 - player2_match_num * 2.5)

    player1_elo_reliable = player1_match_num > 5
    player2_elo_reliable = player2_match_num > 5

    player1_new_elo = player1_elo
    player2_new_elo = player2_elo

    if player2_elo_reliable or not player1_elo_reliable:
        player_progress = player1_prob_post - player1_prob_pre
        player1_new_elo = player1_elo + player1_K * player_progress
    if player1_elo_reliable or not player2_elo_reliable:
        player_progress = player2_prob_post - player2_prob_pre
        player2_new_elo = player2_elo + player2_K * player_progress

    if second_won:
        return player2_new_elo, player1_new_elo
    else:
        return player1_new_elo, player2_new_elo

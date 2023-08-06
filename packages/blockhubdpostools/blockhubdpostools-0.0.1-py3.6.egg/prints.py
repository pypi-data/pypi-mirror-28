import dbtools
import api

"""
This file is used to visually inspect the output of all functions
"""


localnode = dbtools.ArkNode(
    user='postgres',
    password='Dwl1ml12_3#')

address_delegate = 'AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE'
delegate_pubkey = '0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a'
normal_addres = 'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY'


# print(localnode.account_details(address_delegate))
# print(localnode.node_height_details())
# all_delegates = localnode.all_delegates()
# print('length: {}      {}'.format(len(all_delegates), all_delegates))
# current_delegates = localnode.current_delegates()
# print('length: {}      {}'.format(len(current_delegates), current_delegates))
# print(localnode.payouts_to_address(normal_addres))
# print(localnode.transactions_from_address(normal_addres))
# print(localnode.all_votes_by_address(normal_addres))
# print(localnode.calculate_balance_over_time(address_delegate))
# print(localnode.get_last_out_transactions(address_delegate))

#something weird is going on when sorting the current voters
# current_voters = localnode.get_current_voters(address_delegate)
# for i in current_voters:
#     print(current_voters[i]['height'])

# # print(localnode.get_historic_voters(address=address_delegate))
#
actions = localnode.get_events_vote_cluster(address_delegate)
# print(actions)
# # for i in actions:
# #     if actions[i]['event_type'] == 'block':
# #         print(i, actions[i])
#
# #
# # print(api.Network(network='ark').status())


share = localnode.tbw(address_delegate)[0]

for i in share:
    print(i, share[i])


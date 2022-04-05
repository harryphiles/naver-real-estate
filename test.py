# from concurrent.futures import process


# list = [['84.7', '4억 5,000', '광교지웰홈스'], ['84.8', '5억      ', '광교지웰홈스'], ['53.7', '4억 8,000', '힐스테이트광교'], ['77.5', '8억      ', '힐스테이트광교'], ['46.9', '3억 7,000', '에듀하임1309'], ['62.9', '4억 3,000', '에듀하임1309'], ['53.3', '4억      ', '힐스테이트광교중앙역'], ['58.6', '4억 7,000', '힐스테이트광교중앙역'], ['59.1', '4억 6,000', '힐스테이트광교중앙역'], ['59.2', '5억      ', '힐스테이트광교중앙역'], ['59.3', '4억 1,700', '힐스테이트광교중앙역'], ['59.4', '4억      ', '힐스테이트광교중앙역'], ['83.4', '7억 3,000', '힐스테이트광교중앙역']]
# list2 = []
# # for i in list:
# #     try:
# #         print('{:.1}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
# #     except:
# #         print('{:.1}0000'.format(i[1].split()[0]))

# # for i in list:
# #     try:
# #         prc = int('{:.1}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
# #     except:
# #         prc = int('{:.1}0000'.format(i[1].split()[0]))
# #     if prc < 42000:
# #         print('\n')
# #         print(prc)

# for i in list:
#     try:
#         prc = int('{:.1}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
#     except:
#         prc = int('{:.1}0000'.format(i[1].split()[0]))
#     if prc < 42000:
#         list2.append(i)

# x = ''
# for i in range(len(list2)):
#     x += list2[i][0] + " " + list2[i][1] + " " + list2[i][2] + "\n"
# print(x)
#         # if i == 0:
#         #     x += list[i] + "\n"
#         #     x += list2[i][0] + " " + list2[i][1] + "\n"
#         # else:
#         #     x += list2[i][0] + " " + list2[i][1] + "\n"

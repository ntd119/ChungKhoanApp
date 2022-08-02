

von = 20000000
bandau = 20000000

# lai = (bandau * 0.4)/100
#
# print(lai)

for i in range(50):
    bandau += (bandau * 0.4)/100
    bandau += von
    # print(bandau)

print(bandau)
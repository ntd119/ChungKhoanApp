import matplotlib.pyplot as plt

plt.plot([0,1,2,3,4], [1,2,3,4,10], 'go-', label='Python')
plt.plot([0,1,2,3,4], [10,4,3,2,1], 'ro-', label='C#')
plt.plot([2.5,2.5,2.5,1.5,0.5], [1,3,5,7,10], 'bo-', label='Java')
plt.title('Vẽ đồ thị trong Python với Matplotlib')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend(loc='best')
plt.show()


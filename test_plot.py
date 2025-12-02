import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

try:
    print("Attempting to create a test plot...")
    # Create a simple figure
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.set_title("Test Plot")
    
    # Define a simple, absolute path
    file_path = os.path.join(os.getcwd(), 'test_plot.png')
    
    # Save the figure
    plt.savefig(file_path)
    
    print(f"Successfully attempted to save plot to: {file_path}")
    
    # Verify if the file was actually created
    if os.path.exists(file_path):
        print("SUCCESS: The file 'test_plot.png' was created.")
    else:
        print("FAILURE: The file 'test_plot.png' was NOT created.")

except Exception as e:
    print(f"An error occurred during the plotting test: {e}")

import pyautogui
import time
import random
import tkinter as tk
import keyboard
import cv2
import numpy as np



pyautogui.useImageNotFoundException()
screen_width, screen_height = pyautogui.size()

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def searchAllTemplate(templatePath, fromPos):
    screenshot = pyautogui.screenshot()
    image_np = np.array(screenshot)
    
    template = cv2.imread(templatePath)

    # Convert images to grayscale
    main_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Apply template matching
    result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Set a threshold to identify matches
    threshold = 0.50
    locations = np.where(result >= threshold)

    # Apply non-maximum suppression
    rectangles = []
    for loc in zip(*locations[::-1]):
        x, y = loc
        width, height = template.shape[1], template.shape[0]
        rectangles.append((x, y, x + width, y + height))

    # Apply non-maximum suppression to get only the most confident match
    rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)

    # Initialize minimum distance to a large value
    min_distance = float('inf')
    min_distance_point = None

    # Iterate over rectangles to find the minimum distance
    for rect in rectangles:
        x, y, x_plus_w, y_plus_h = rect
        center = ((x + x_plus_w) // 2, (y + y_plus_h) // 2)
        
        # Calculate distance between fromPos and the center of the rectangle
        distance = calculate_distance(fromPos, center)
        
        if distance < min_distance:
            min_distance = distance
            min_distance_point = center
    
    pyautogui.click(min_distance_point[0], min_distance_point[1], clicks=1, interval=0.05, button='left')
    return min_distance
    

def searchTemplate(templatePath):
    screenshot = pyautogui.screenshot()
    image_np = np.array(screenshot)
    
    template = cv2.imread(templatePath)

    # Convert images to grayscale
    main_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Apply template matching
    result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    # Find the location of the maximum value in the result matrix
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    match_threshold = 0

    if max_val >= match_threshold:
        # Get the coordinates of the center of the rectangle with the highest match
        x, y = max_loc
        width, height = template.shape[1], template.shape[0]
        center_x, center_y = x + width // 2, y + height // 2

        # Draw a rectangle around the highest match
        cv2.rectangle(image_np, (x, y), (x + width, y + height), (0, 255, 0), 2)

    
        # Click on the center of the box
        
        pyautogui.click(center_x, center_y)
        
        
        return (center_x,center_y)
    else:
        return None


def SeachAndClickConfirmBtt():
    screenshot = pyautogui.screenshot()
    image_np = np.array(screenshot)
            
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([98, 50, 50])
    upper_blue = np.array([139, 255, 255])
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on aspect ratio and bounding box dimensions
    max_aspect_ratio = 5  # Adjust as needed
    min_width =  100  # Adjust as needed
    min_height = 50  # Adjust as needed
            
    filtered_contours = [
        cnt for cnt in contours
        if min_width < cv2.boundingRect(cnt)[2] < image_np.shape[1]
        and min_height < cv2.boundingRect(cnt)[3] < image_np.shape[0]
        and min_width < cv2.boundingRect(cnt)[3] * max_aspect_ratio < image_np.shape[1]
    ]
    for cnt in filtered_contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx, cy)
            pyautogui.click(cx, cy, clicks=1, interval=0.05, button='left')

def Refresh(randomDuration):
    rand = random.uniform(300,randomDuration)
    
    resultCv = searchTemplate('covenant.PNG')
    resultMystic = searchTemplate('mystic.PNG')
    if resultCv == None and resultMystic == None:
        start_x, start_y = screen_width*2/3, screen_height*2/3
        drag_distance = random.randrange(350, 500)
        # Perform a mouse click at the starting position
        pyautogui.click(start_x, start_y)
        # Move the mouse to the new position to simulate dragging
        end_x, end_y = start_x , start_y - drag_distance
        time.sleep(rand/1000)
        pyautogui.dragTo(end_x, end_y, duration=0.3)
        resultCv = searchTemplate('covenant.PNG')
        resultMystic = searchTemplate('mystic.PNG')

    
    if resultCv == None and resultMystic == None:
        RefreshShop(rand)
        return
    
    if resultCv !=None :
        searchAllTemplate('buyBtt.png', resultCv)
        time.sleep(rand/1000)

        searchTemplate('Buy_button_Covenant.PNG')
        time.sleep(rand/1000)


    if resultMystic != None:
        searchAllTemplate('buyBtt.png',resultMystic)
        time.sleep(rand/1000)

        searchTemplate('Buy_button_Mystic.PNG')
        time.sleep(rand/1000)


    
def SeachAndBuyMystic():
    screenshot = pyautogui.screenshot()
    image_np = np.array(screenshot)
            
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    lower_red = np.array([130, 50, 50])  # Lower HSV values for pinkish-red
    upper_red = np.array([252, 150, 100])  # Upper HSV values for pinkish-red

    mask = cv2.inRange(hsv_image, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    minWidth = 50
    minRatio = 0.5
    # Filter contours based on aspect ratio and bounding box dimensions
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
    
        ratio = w / h if w < h else h / w
        range = w if w < h else h
    
        if (w+h)/2 > minWidth and ratio > minRatio:
            cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)

    
    cv2.imshow('Filtered Contours with Centers', image_np)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def RefreshShop(rand):
    searchTemplate('refresh_button.PNG')
    time.sleep(rand/1000) 
    SeachAndClickConfirmBtt()
    time.sleep(rand/500)
    


class App:
    def __init__(self, master):
        self.master = master
        master.title("E7 secret shop refresh autogui")

        self.label = tk.Label(master, text="Disclaimer: Smilegate bans macro, uses at your own risk.")
        self.label.pack(pady=5)
        self.label = tk.Label(master, text="Make sure the game is in fullscreen before you start\nMove mouse to one of 4 corners to stop")                                                 
        self.label.pack(pady=5)

        self.button = tk.Button(master, text="Start", command=self.on_button_click)
        self.button.pack(pady=5)
        
        self.labelDuration = tk.Label(master, text="Duration between clicks: A random value between\n300 and 400 ms")
        self.labelDuration.pack(side=tk.TOP, padx=10)

        self.scaleDuration = tk.Scale(master, from_=400, to=600, orient=tk.HORIZONTAL, command=self.on_scale_change)
        
        self.randomDuration = 400
        self.scaleDuration.pack(side=tk.TOP, padx=10)

     

        keyboard.on_press(self.on_key_press)
        
        master.geometry("500x300")
        master.resizable(False, False)

    def on_scale_change(self, value):
        self.labelDuration.config(text=f"Duration between clicks: A random value between\n300 and {value} ms")
        self.randomDuration = int(value)

    def on_scaleConfidence_change(self, value):
        try:
            confidence = float(value)
            self.confidence = confidence / 100.0

        except ValueError:
        # Handle the case where the conversion to float fails (e.g., if the value is not a valid number)
            print("Invalid confidence value:", value)

    def on_key_press(self, event):
        # Check if the pressed key is the Escape key or '1'
        if event.name == 'esc' or event.name == '1':
           # Take a screenshot of the entire screen
            searchTemplate('Mystic')
            
        
    def on_button_click(self):
        self.master.iconify()
        while True:
            Refresh(self.randomDuration)
            if pyautogui.position in [(0,0),(screen_width,0),(0,screen_height),(screen_width,screen_height)]:
                break
                
        

    def on_randomizeClick_enable(self):
        pass
    
def main():
    root = tk.Tk()
    app = App(root)
    #pyautogui.moveTo(500, 500, duration=1)
    root.mainloop()

if __name__ == "__main__":
    main()





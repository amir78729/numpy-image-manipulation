import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS

#################### Functions ####################
#img is a 3 * 4M matrix and M = (x1 + ... + x4M)/n
def calculate_mean(img):
    n = img.shape[0]
    mean =[[.0 , .0 , .0]]
    for pixel in range(img.shape[0]):
        mean = mean + img[pixel]
    mean = mean / n
    return mean

#img is a 3 * 4M matrix, ^Xi = Xi - M (M = mean)
def calculate_covariance_matrix(img, m):
    n = img.shape[0]
    B = img
    for pixel in range(img.shape[0]):
        B[pixel] = B[pixel] - m
    B = B.transpose()
    s = (B.dot(B.transpose()))/(n-1)
    return s

#img is a 3 * 4M matrix, s is covariance
def calculate_variance_matrix(s):
    variance = np.array([[.0 , .0 , .0]])
    for v in range(3):
        variance[0][v] = s[v][v]
    return variance

#a function that calculates the total cariance
def calculate_total_variance(variance_matrix):
    total_variance = .0
    for v in range(3):
        total_variance = total_variance + variance_matrix[0][v]
    return total_variance

#showing covariance matrix status
def analysis_of_covariance_matrix(s):
    print('   >>> COVARIANCES ANALYSIS:')
    for i in range(s.shape[0]):
        for j in range(s.shape[1]):
            if(i != j):
                print("      >>> COV( X",i+1,", X",j+1,")=",round(s[i][j],4),end = " \t")
                if round(s[i][j],4) == 0:##########################
                    print("->\tX",i+1,"and X",j+1, "are UNCORRELATED.")
                else:
                    print("")
    print('   >>> VARIANCES ANALYSIS:')
    variance_matrix = calculate_variance_matrix(s)
    for v in range(variance_matrix.shape[1]):
        print("      >>> VAR( X",v+1,")=",round(variance_matrix[0][v], 4))

#print matrixes
def print_matrix(matrix):
    matrix = matrix.transpose()
    for row in range(matrix.shape[0]):
        if row == 0:
            print('  [[', end = ' ')
        else:
            print('   [', end = ' ')
        for col in range(matrix.shape[1]):
            print(round(matrix[row][col], 4), end ='   \t')
        if row == matrix.shape[0] - 1:
            print(']]')
        else:
            print(']')

#print matrixes rounded manually
def print_matrix_with_manually_floating_digits(matrix, number_of_floating_digits):
    matrix = matrix.transpose()
    for row in range(matrix.shape[0]):
        if row == 0:
            print('  [[', end = ' ')
        else:
            print('   [', end = ' ')
        for col in range(matrix.shape[1]):
            print(round(matrix[row][col], number_of_floating_digits), end ='   \t')
        if row == matrix.shape[0] - 1:
            print(']]')
        else:
            print(']')

#calculating the eigenvalues of matrix
def calculate_eigenvalues(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvalues
    
#calculating the normal eigenvectors of matrix
def calculate_eigenvectors(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvectors

#creating the diagonal matrix of eigenvalues
def catculate_d_matrix(eigenvalues_matrix):
    d_matrix = np.array([[.0,.0,.0],[.0,.0,.0],[.0,.0,.0]])
    for i in range(3):
        d_matrix[i][i] = eigenvalues_matrix[i]
    return d_matrix

#a function that prints metadata and alse tell us if an image has no metadata
def print_metadata(image):
    has_metadata = False
    exifdata = image.getexif()
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            has_metadata = True
            data = data.decode()
        print('   >>>',f"{tag:25}: {data}")
    return has_metadata

####################    Main   ####################
#mode = 1: ready image
#mode = 2: user image
def image_proccessing(mode):
    print('--------------------------------------------------------------------')
    print('>>> Q1: SELECTING IMAGE :')
    #mode = 1: ready image
    if mode == 1: 
        #open image
        image_name = 'butterfly in Shiraz.jpg' #default photo number 1
        # image_name = 'poopak.jpg' #default photo number 2 (+ metadata) <<UNCOMMENT!!>>
    #mode = 2: user image
    else: 
        image_name = str(input("Enter the name of your image (Make sure that your image is placed\nin the same directory is this python file):")) 

    try:
        original_image = Image.open(image_name)
        print('   >>> IMAGE \"',image_name, '\" HAS BEEN SELECTED.')

        print('--------------------------------------------------------------------')
        print('>>> Q2: CONVERTING IMAGE TO MATRIX :')
        #resize the image into 2000px * 2000px
        h = w = 2000
        image = original_image.resize((h, w))
        #convert image into a 3*4M matrix
        image_matrix = np.array(image) 
        image_matrix.resize((h * w, 3))
        print('   >>> IMAGE \"',image_name, '\" HAS BEEN CONVERTED TO A 3*',end="")
        print(h*w,'MATRIX:\n')
        print(image_matrix.transpose())
        print("")

        print('--------------------------------------------------------------------')
        print('>>> Q3: META DATAS :')
        try:
            if (not print_metadata(original_image)):
                print('   >>> METADATA NOT FOUND!')
        except:
            print('   >>> METADATA NOT FOUND!')

        print('--------------------------------------------------------------------')
        print('>>> Q4: CALCULATING MEAN MATRIX:\n')
        mean = calculate_mean(image_matrix)
        print_matrix(mean)
        print("")

        print('--------------------------------------------------------------------')
        print('>>> Q5: CALCULATING COVARIANCE MATRIX:\n')
        covariance = calculate_covariance_matrix(image_matrix, mean)
        print_matrix (covariance)
        print("")

        print('--------------------------------------------------------------------')
        print('>>> Q6: COVARIANCE MATRIX ANALYSIS:')
        analysis_of_covariance_matrix(covariance)

        print('--------------------------------------------------------------------')
        print('>>> Q7: REDUCING THE DIMENTION OF MULTIVARIATE DATA:')
        print('   >>> CATCULATING EIGENVALUES:')
        eigenvalues = calculate_eigenvalues(covariance)
        for i in range(3):
            print("      >>> eigenvalue #",end = "")
            print(i+1,end="")
            print(" =", round(eigenvalues[i],4))
        print('   >>> CREATING D MATRIX:\n')
        d_matrix = catculate_d_matrix(eigenvalues)
        print(d_matrix)
        print("")
        print('   >>> CATCULATING THE TOTAL VARIANCE:')
        print('      >>> IF S = P x D x P(T) THEN TOTAL_VARIANCE = tr(D)')
        print('          =',d_matrix[0][0],'+',d_matrix[1][1],'+',d_matrix[2][2])
        total_variance = calculate_total_variance(calculate_variance_matrix(covariance))
        print("          =",total_variance)
        for i in range(3):
            print('   >>> x',i+1,':',d_matrix[i][i],'/',total_variance,'=',round(100*d_matrix[i][i]/total_variance,2),'%')

        print('--------------------------------------------------------------------')
        print('>>> Q8: PRINCIPAL COMPONENT ANALYSIS:')
        print('   >>> CATCULATING EIGENVALUES (P):\n')
        p = calculate_eigenvectors(covariance)
        print_matrix_with_manually_floating_digits(p,4)
        print('')
        print('   >>> CATCULATING P^(-1):\n')
        p_inverse = np.linalg.inv(p)
        print_matrix_with_manually_floating_digits(p_inverse,4)
        print('')
        print('   >>> CATCULATING Y = P^(-1) * X:')
        y = p_inverse.dot(image_matrix.transpose())
        print(y)
        y = y.transpose()
        print('   >>> CONVERTING MATRIX TO IMAGE:')
        #save the new resized image in the same directory
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for pixel in range(h*w):
            data[int(pixel/w),pixel%w] = [y[pixel][0],y[pixel][1],y[pixel][2]]
        result = Image.fromarray(data, 'RGB')
        print('   >>> SAVING IMAGE:')
        result_name = 'resized_image.png'
        result.save(result_name)
        print('   >>> SHOWING IMAGE:')
        result.show()
    except:
        print('   >>> IMAGE NOT FOUND!')

# the relation between program and the user
def start():
    print('*******************************************************')
    print('**************** Applied Linear Algebra ***************')
    print('********************** Project #2 *********************')
    print('**************** Amirhossein Alibakhshi ***************')
    print('********************** id:9731096 *********************')
    print('*******************************************************\n')
    print('Hi! How do you want to work with this ')
    print('program?')
    print(' 1 - using ready image')
    print(' 2 - using another image')
    print('-1 - exit the program')
    command = int(input('please enter your choice:  '))
    while command != -1:
        if command == 1 or command == 2:
            image_proccessing(command)
            print('Now how do you want to work with this ')
            print('program?')
            print('1 - using ready image')
            print('2 - using another image')
            print('-1 - exit the program')
            command = int(input('please enter your choice:  '))
        else:
            command = int(input('please enter a valid number:  '))
    print('bye:)')

#start the program
start()

def checkIfSeatingIsPossible(students, noOfCls, row, col):
    totalSeats = row * col * noOfCls
    studentCounts = [x[1] for x in students]
    majority = max(studentCounts)
    totalStudents = sum(studentCounts)
    if totalStudents > totalSeats or majority > totalSeats / 2:
        return False
    else:
        return True


def setSeatingInCls(cls, student, row, col):
    ok = False
    for std in student:
        if std[1] > 0:
            ok = True
            break
    if ok == False:
        return False

    for i in range(row):
        for j in range(col):
            for std in students:
                if std[1] > 0:
                    if j - 1 > -1 and std[0][0:6] == cls[i][j - 1][0:6]:
                        continue
                    if j + 1 < col and std[0][0:6] == cls[i][j + 1][0:6]:
                        continue
                    if i - 1 > -1 and std[0][0:6] == cls[i - 1][j][0:6]:
                        continue
                    if i + 1 < row and std[0][0:6] == cls[i + 1][j][0:6]:
                        continue
                    cls[i][j] = f"{std[0]}0{std[2]:02}"
                    std[2] += 1
                    std[1] -= 1
                    break
    return True


def setSeating(students, noOfCls, row, col, clsNames):
    if checkIfSeatingIsPossible(students, noOfCls, row, col) == False:
        print("Seating Not Possible")
        return

    clsNo = 0
    while noOfCls > 0:
        cls = [["----------" for _ in range(col)] for _ in range(row)]
        if setSeatingInCls(cls, students, row, col):
            print(clsNames[clsNo])
            for i in cls:
                print(i)
            print()
        noOfCls -= 1
        clsNo += 1


if __name__ == "__main__":
    students = []
    noOfSubjects = int(input())
    while noOfSubjects > 0:
        cls, r1, r2 = input().split()
        students.append([cls, int(r2) - int(r1) + 1, int(r1)])
        noOfSubjects -= 1
    students.sort(key=lambda x: x[1], reverse=True)

    noOfCls = int(input())
    row, col = (int(x) for x in input().split())
    clsNames = [name for name in input().split()]

    setSeating(students, noOfCls, row, col, clsNames)


# 4
# adr20cs 1 59
# adr20ec 1 36
# adr20me 1 80
# adr20ee 1 20
# 7
# 5 6
# 301 302 303 404 405 501 514 515 518 519

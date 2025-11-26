#include <iostream>
#include <cmath>

// Legacy Matrix Class - No Templates, Fixed 4x4
class Matrix4 {
public:
    float* m; // Pointer for data array

    Matrix4() {
        m = new float[16];
        identity();
    }

    ~Matrix4() {
        delete[] m;
    }

    void identity() {
        for(int i=0; i<16; ++i) m[i] = 0.0f;
        m[0] = m[5] = m[10] = m[15] = 1.0f;
    }

    // Multiply this matrix by another
    void multiply(Matrix4* other) {
        float* temp = new float[16];

        for (int r = 0; r < 4; r++) {
            for (int c = 0; c < 4; c++) {
                temp[r*4 + c] = 0.0f;
                for (int k = 0; k < 4; k++) {
                    // Row-major calculation
                    temp[r*4 + c] += m[r*4 + k] * other->m[k*4 + c];
                }
            }
        }

        // Copy back
        for(int i=0; i<16; ++i) m[i] = temp[i];
        delete[] temp;
    }

    void setTranslation(float x, float y, float z) {
        // Direct index access, hard to read without context
        m[12] = x;
        m[13] = y;
        m[14] = z;
    }

    float getDeterminant() {
        // Simplified determinant for 3x3 upper left
        return m[0] * (m[5] * m[10] - m[6] * m[9]) -
               m[1] * (m[4] * m[10] - m[6] * m[8]) +
               m[2] * (m[4] * m[9] - m[5] * m[8]);
    }
};

int main() {
    Matrix4* matA = new Matrix4();
    Matrix4* matB = new Matrix4();

    matA->setTranslation(10.0f, 5.0f, 0.0f);
    matB->setTranslation(2.0f, 3.0f, 1.0f);

    matA->multiply(matB);

    std::cout << "Det: " << matA->getDeterminant() << std::endl;

    delete matA;
    delete matB;
    return 0;
}

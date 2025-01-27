from math import pi, acos

config = {
    "l_chassis": 184e-3,
    "w_chassis": 57.5e-3,
    "l_shoulder": 29.5e-3,
    "l_upper": 63.9e-3,
    "l_lower": 82.17e-3,
    "r_foot": 4.9e-3
}


def gamma(c):
    return acos((config["l_upper"]**2+config["l_lower"]**2-(c*1e-3)**2)/(2*config["l_upper"]*config["l_lower"]))


config["servos"] = {
    "RBS": {
        "port": 0,
        "pwm_vals": [
            4800,
            1800,
            7800
        ],
        "ang_vals": [
            0,
            -pi/2,
            pi/2
        ]
    },
    "RBU": {
        "port": 1,
        "pwm_vals": [
            5000,
            8200
        ],
        "ang_vals": [
            0,
            pi/2
        ]
    },
    "RBL": {
        "port": 2,
        "pwm_vals": [
            2000,
            4700,
            6700
        ],
        "ang_vals": [
            gamma(59.5),
            pi/2,
            gamma(139)
        ]
    },
    "LBS": {
        "port": 4,
        "pwm_vals": [
            5200,
            2200,
            8200
        ],
        "ang_vals": [
            0,
            -pi/2,
            pi/2
        ]
    },
    "LBU": {
        "port": 5,
        "pwm_vals": [
            4700,
            1600
        ],
        "ang_vals": [
            0,
            pi/2
        ]
    },
    "LBL": {
        "port": 6,
        "pwm_vals": [
            2700,
            4300,
            7000
        ],
        "ang_vals": [
            gamma(139),
            pi/2,
            gamma(59.5)
        ]
    },
    "RFS": {
        "port": 8,
        "pwm_vals": [
            5500,
            8500,
            2500
        ],
        "ang_vals": [
            0,
            -pi/2,
            pi/2
        ]
    },
    "RFU": {
        "port": 9,
        "pwm_vals": [
            2700,
            5900
        ],
        "ang_vals": [
            0,
            pi/2
        ]
    },
    "RFL": {
        "port": 10,
        "pwm_vals": [
            2500,
            4900,
            7000
        ],
        "ang_vals": [
            gamma(59.5),
            pi/2,
            gamma(139)
        ]
    },
    "LFS": {
        "port": 12,
        "pwm_vals": [
            5300,
            8300,
            2300
        ],
        "ang_vals": [
            0,
            -pi/2,
            pi/2
        ]
    },
    "LFU": {
        "port": 13,
        "pwm_vals": [
            8000,
            4900
        ],
        "ang_vals": [
            0,
            pi/2
        ]
    },
    "LFL": {
        "port": 14,
        "pwm_vals": [
            6700,
            4800,
            2000
        ],
        "ang_vals": [
            gamma(59.5),
            pi/2,
            gamma(139)
        ]
    }
}

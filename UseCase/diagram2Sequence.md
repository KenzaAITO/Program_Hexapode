sequenceDiagram
    participant User
    participant KeyboardHandler
    participant MovementLibrary
    participant DynamixelSDK
    participant Servomotor1
    participant Servomotor2
    participant Servomotor3

    %% Forward Movement
    User->>KeyboardHandler: Press Up Arrow
    KeyboardHandler->>MovementLibrary: Forward command
    MovementLibrary->>DynamixelSDK: Send move forward signal
    DynamixelSDK->>Servomotor1: Set forward position
    DynamixelSDK->>Servomotor2: Set forward position
    DynamixelSDK->>Servomotor3: Set forward position
    Servomotor1-->>DynamixelSDK: Forward position reached
    Servomotor2-->>DynamixelSDK: Forward position reached
    Servomotor3-->>DynamixelSDK: Forward position reached

    %% Backward Movement
    User->>KeyboardHandler: Press Down Arrow
    KeyboardHandler->>MovementLibrary: Backward command
    MovementLibrary->>DynamixelSDK: Send move backward signal
    DynamixelSDK->>Servomotor1: Set backward position
    DynamixelSDK->>Servomotor2: Set backward position
    DynamixelSDK->>Servomotor3: Set backward position
    Servomotor1-->>DynamixelSDK: Backward position reached
    Servomotor2-->>DynamixelSDK: Backward position reached
    Servomotor3-->>DynamixelSDK: Backward position reached

    %% Right Movement
    User->>KeyboardHandler: Press Right Arrow
    KeyboardHandler->>MovementLibrary: Right command
    MovementLibrary->>DynamixelSDK: Send move right signal
    DynamixelSDK->>Servomotor1: Set right position
    DynamixelSDK->>Servomotor2: Set right position
    DynamixelSDK->>Servomotor3: Set right position
    Servomotor1-->>DynamixelSDK: Right position reached
    Servomotor2-->>DynamixelSDK: Right position reached
    Servomotor3-->>DynamixelSDK: Right position reached

    %% Left Movement
    User->>KeyboardHandler: Press Left Arrow
    KeyboardHandler->>MovementLibrary: Left command
    MovementLibrary->>DynamixelSDK: Send move left signal
    DynamixelSDK->>Servomotor1: Set left position
    DynamixelSDK->>Servomotor2: Set left position
    DynamixelSDK->>Servomotor3: Set left position
    Servomotor1-->>DynamixelSDK: Left position reached
    Servomotor2-->>DynamixelSDK: Left position reached
    Servomotor3-->>DynamixelSDK: Left position reached

    %% Rotate Movement
    User->>KeyboardHandler: Press "O" key
    KeyboardHandler->>MovementLibrary: Rotate command
    MovementLibrary->>DynamixelSDK: Send rotate signal
    DynamixelSDK->>Servomotor1: Set rotate position
    DynamixelSDK->>Servomotor2: Set rotate position
    DynamixelSDK->>Servomotor3: Set rotate position
    Servomotor1-->>DynamixelSDK: Rotate position reached
    Servomotor2-->>DynamixelSDK: Rotate position reached
    Servomotor3-->>DynamixelSDK: Rotate position reached

import os
srcFldr = "wy-simplified-23-1-0-HighRise"
targetFldr = "wy-simplified-23-1-0-HighRise-LWR"
if not os.path.exists(targetFldr):
    os.makedirs(targetFldr)

# 56, 44, 50, 38

linesToADD = '''\
SurfaceProperty:SurroundingSurfaces,
    SrdSurfs:Surface 56,  !- Name
    ,                     !- Sky View Factor
    ,                        !- Sky Temperature Schedule Name
    ,                        !- Ground View Factor
    ,                        !- Ground Temperature Schedule Name
    SurroundingSurface1,     !- Surrounding Surface 1 Name
    0.5,                     !- Surrounding Surface 1 View Factor
    Srf-Surface 56-Tmp;  !- Surrounding Surface 1 Temperature Schedule Name

Schedule:Compact,
    Srf-Surface 56-Tmp,  !- Name
    Temperature,             !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,            !- Field 3
    19.0;                    !- Field 4

SurfaceProperty:SurroundingSurfaces,
    SrdSurfs:Surface 44,  !- Name
    ,                     !- Sky View Factor
    ,                        !- Sky Temperature Schedule Name
    ,                        !- Ground View Factor
    ,                        !- Ground Temperature Schedule Name
    SurroundingSurface1,     !- Surrounding Surface 1 Name
    0.5,                     !- Surrounding Surface 1 View Factor
    Srf-Surface 44-Tmp;  !- Surrounding Surface 1 Temperature Schedule Name

Schedule:Compact,
    Srf-Surface 44-Tmp,  !- Name
    Temperature,             !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,            !- Field 3
    19.0;                    !- Field 4
        
SurfaceProperty:SurroundingSurfaces,
    SrdSurfs:Surface 50,  !- Name
    ,                     !- Sky View Factor
    ,                        !- Sky Temperature Schedule Name
    ,                        !- Ground View Factor
    ,                        !- Ground Temperature Schedule Name
    SurroundingSurface1,     !- Surrounding Surface 1 Name
    0.5,                     !- Surrounding Surface 1 View Factor
    Srf-Surface 50-Tmp;  !- Surrounding Surface 1 Temperature Schedule Name

Schedule:Compact,
    Srf-Surface 50-Tmp,  !- Name
    Temperature,             !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,            !- Field 3
    19.0;                    !- Field 4

SurfaceProperty:SurroundingSurfaces,
    SrdSurfs:Surface 38,  !- Name
    ,                     !- Sky View Factor
    ,                        !- Sky Temperature Schedule Name
    ,                        !- Ground View Factor
    ,                        !- Ground Temperature Schedule Name
    SurroundingSurface1,     !- Surrounding Surface 1 Name
    0.5,                     !- Surrounding Surface 1 View Factor
    Srf-Surface 38-Tmp;  !- Surrounding Surface 1 Temperature Schedule Name

Schedule:Compact,
    Srf-Surface 38-Tmp,  !- Name
    Temperature,             !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,            !- Field 3
    19.0;                    !- Field 4

SurfaceProperty:LocalEnvironment,
    LocEnv:Surface 44,    !- Name
    Surface 44,           !- Exterior Surface Name
    ,                        !- External Shading Fraction Schedule Name
    SrdSurfs:Surface 56,  !- Surrounding Surfaces Object Name
    ;                        !- Outdoor Air Node Name

SurfaceProperty:LocalEnvironment,
    LocEnv:Surface 56,    !- Name
    Surface 56,           !- Exterior Surface Name
    ,                        !- External Shading Fraction Schedule Name
    SrdSurfs:Surface 44,  !- Surrounding Surfaces Object Name
    ;                        !- Outdoor Air Node Name

SurfaceProperty:LocalEnvironment,
    LocEnv:Surface 50,    !- Name
    Surface 50,           !- Exterior Surface Name
    ,                        !- External Shading Fraction Schedule Name
    SrdSurfs:Surface 38,  !- Surrounding Surfaces Object Name
    ;                        !- Outdoor Air Node Name

SurfaceProperty:LocalEnvironment,
    LocEnv:Surface 38,    !- Name
    Surface 38,           !- Exterior Surface Name
    ,                        !- External Shading Fraction Schedule Name
    SrdSurfs:Surface 50,  !- Surrounding Surfaces Object Name
    ;                        !- Outdoor Air Node Name
    '''

for file in os.listdir(srcFldr):
    with open(os.path.join(srcFldr, file), 'r') as f:
        lines = f.readlines()
    
    lines = linesToADD + "\n" + "".join(lines)
    with open(os.path.join(targetFldr, file), 'w') as f:
        f.write(lines)
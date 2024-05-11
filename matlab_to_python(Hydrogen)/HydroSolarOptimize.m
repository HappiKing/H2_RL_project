%{
function [Pgrid,Phydro,Ehydro] = battSolarOptimize(N, dt, Ppv, Pload, Einit, Cost, FinalWeight, hydroMinMaxEmax, hydroMinMaxEmin, hydroMinMaxPmin, hydroMinMaxPmax, elecEff, fuelEff, F, V)

    % Minimize the cost of power from the grid while meeting load with power 
    % from PV, battery, and grid 

    prob = optimproblem;

    % Decision variables
    PgridV = optimvar('PgridV', N);
    PhydroV = optimvar('PhydroV',N,'LowerBound',hydroMinMaxPmin,'UpperBound',hydroMinMaxPmax);
    EhydroV = optimvar('EhydroV',N,'LowerBound',hydroMinMaxEmin,'UpperBound',hydroMinMaxEmax);
    PgridDelta = optimvar('gridDelta',N-1);

    % Minimize cost of electricity from the grid
    prob.ObjectiveSense = 'minimize';
    prob.Objective = dtCostPgridV - FinalWeight((((EhydroV(N)elecEff)/(2F))2)VfuelEff)/1000 + sum(PgridDelta);

    % Power input/output to battery
    prob.Constraints.energyBalance = optimconstr(N);
    prob.Constraints.energyBalance(1) = EhydroV(1) == Einit;
    prob.Constraints.energyBalance(2:N) = EhydroV(2:N) == EhydroV(1:N-1) - PhydroV(1:N-1) * dt;

    % Satisfy power load with power from PV, grid, and battery
    prob.Constraints.loadBalance = Ppv + PgridV + PhydroV == Pload;

    % Track change from period to period to electricity from the grid
    prob.Constraints.deltaPlus = PgridV(2:N) - PgridV(1:N-1) <= PgridDelta;
    prob.Constraints.deltaMinus = PgridV(1:N-1) - PgridV(2:N) <= PgridDelta;

    % Solve the linear program
    options = optimoptions(prob,'Display','none');
    [values, ~, exitflag] = solve(prob, 'Options', options);

    % Parse optimization results
    if exitflag <= 0
        Pgrid = zeros(N, 1);
        Phydro = zeros(N, 1);
        Ehydro = zeros(N, 1);
    else
        Pgrid = values.PgridV;
        Phydro = values.PhydroV;
        Ehydro = values.EhydroV;
    end

%}
function [Pgrid,Pbatt,Ebatt] = battSolarOptimize(N,dt,Ppv,Pload,Einit,Cost,FinalWeight,batteryMinMaxEmax, batteryMinMaxEmin, batteryMinMaxPmin, batteryMinMaxPmax)

% Minimize the cost of power from the grid while meeting load with power 
% from PV, battery and grid 

prob = optimproblem;

% Decision variables
PgridV = optimvar('PgridV',N);
PbattV = optimvar('PbattV',N,'LowerBound',batteryMinMaxPmin,'UpperBound',batteryMinMaxPmax);
EbattV = optimvar('EbattV',N,'LowerBound',batteryMinMaxEmin,'UpperBound',batteryMinMaxEmax);

% Minimize cost of electricity from the grid
prob.ObjectiveSense = 'minimize';
prob.Objective = dt * Cost' *PgridV - FinalWeight * EbattV(N);

% Power input/output to battery
prob.Constraints.energyBalance = optimconstr(N);
prob.Constraints.energyBalance(1) = EbattV(1) == Einit; % 여기가 초기 값 선언 
% prob.Constraints.energyBalance(2:N) = EbattV(2:N) == EbattV(1:N-1) - PbattV(1:N-1)*dt;

% 충전 효율과 방전 효율을 별도의 제약 조건으로 설정
efficiencyCharge = 0.7 * 33.33;
efficiencyDischarge = 2;

% 방전 상태 (PbattV >= 0)
prob.Constraints.dischargeEfficiency = optimconstr(N);  
prob.Constraints.dischargeEfficiency = EbattV(2:N) >= EbattV(1:N-1) - PbattV(1:N-1) * dt * efficiencyDischarge;

% % 충전 상태 (PbattV < 0)
prob.Constraints.chargeEfficiency = optimconstr(N);             
prob.Constraints.chargeEfficiency = EbattV(2:N) <= EbattV(1:N-1) - (((PbattV(1:N-1) * dt * efficiencyCharge) / 1000) * 33.33);

% Satisfy power load with power from PV, grid and battery
prob.Constraints.loadBalance = Ppv + PgridV + PbattV == Pload;

% Solve the linear program
options = optimoptions(prob.optimoptions,'Display','none');
[values,~,exitflag] = solve(prob,'Options',options);

% Parse optmization results
if exitflag <= 0
    Pgrid = zeros(N,1);
    Pbatt = zeros(N,1);
    Ebatt = zeros(N,1);
else
    Pgrid = values.PgridV;
    Pbatt = values.PbattV;
    Ebatt = values.EbattV;
end

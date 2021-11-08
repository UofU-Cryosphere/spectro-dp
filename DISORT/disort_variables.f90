module disort_variables
  implicit none 

  LOGICAL DOPROB( 17 )
  DATA DOPROB / 17*.TRUE. /
  LOGICAL  USRANG, USRTAU, ONLYFL, PRNT(5), &
           PLANK, LAMBER, DELTAMPLUS, DO_PSEUDO_SPHERE
  INTEGER  IBCND, NMOM, NLYR, NUMU, NSTR, NPHI, NTAU
  INTEGER  NUMU_O
  LOGICAL  DEBUG
  real(kind=4) :: ACCUR, ALBEDO, BTEMP, FBEAM, FISOT, &
                  PHI0, TEMIS, TTEMP, WVNMLO, WVNMHI, UMU0 
  real(kind=4),parameter :: EARTH_RADIUS = 6371.0     
  DATA PRNT  / .TRUE., 3*.FALSE., .TRUE. /

  INTEGER   BRDF_TYPE
  REAL      BRDF_ARG(4)
  LOGICAL   DO_SHADOW
  REAL      WIND_SPD, REFRAC_INDEX
  REAL      B0, HH, W
  REAL      K_VOL, K_ISO, K_GEO
  REAL      RHO_0, KAPPA, G, H0
  REAL      FLUX_UP, DFDTAU
  INTEGER   NMUG
  REAL      BDREF
  EXTERNAL  BDREF

  real(kind=4),dimension(:),allocatable     :: DTAUC, PHI, SSALB, TEMPER, UMU, UTAU                             
  real(kind=4),dimension(:,:),allocatable   :: PMOM          
  real(kind=4),dimension(:,:,:),allocatable :: RHOQ, RHOU 
  real(kind=4),dimension(:),allocatable     :: EMUST, BEMST   
  real(kind=4),dimension(:,:),allocatable   :: RHO_ACCURATE                             
  real(kind=4),dimension(:),allocatable     :: RFLDIR, RFLDN, FLUP, DFDT, UAVG, ALBMED, TRNMED
  real(kind=4),dimension(:,:,:),allocatable :: UU
  real(kind=4),dimension(:),allocatable     :: H_LYR

  contains 

  subroutine allocate_disort_allocatable_arrays(NLYR, NMOM, NSTR, NUMU, NPHI, NTAU)
    implicit none
    integer,intent(in) :: NLYR, NMOM, NSTR, NUMU, NPHI, NTAU 

    allocate( DTAUC( NLYR ), SSALB( NLYR ), PMOM( 0:NMOM, NLYR ), &
              TEMPER( 0:NLYR ), UTAU( NTAU ), UMU( NUMU ), PHI( NPHI ), H_LYR( 0:NLYR ) )  
    allocate( RHOQ(NSTR/2, 0:NSTR/2, 0:(NSTR-1)), RHOU(NUMU, 0:NSTR/2, 0:(NSTR-1)), &
              EMUST(NUMU), BEMST(NSTR/2), RHO_ACCURATE(NUMU, NPHI) )                
    allocate( RFLDIR( NTAU ), RFLDN( NTAU ), FLUP( NTAU ), DFDT( NTAU ), UAVG( NTAU ),&
              ALBMED( NUMU ), TRNMED( NUMU ), UU( NUMU, NTAU, NPHI ) )   
    DTAUC = 0.0; SSALB = 0.0; PMOM = 0.0; TEMPER = 0.0; UTAU = 0.0; UMU = 0.0; PHI = 0.0;
    H_LYR = 0.0; RHOQ = 0.0; RHOU = 0.0; EMUST = 0.0; BEMST = 0.0; RHO_ACCURATE = 0.0;
    RFLDIR = 0.0; RFLDN = 0.0; FLUP = 0.0; DFDT = 0.0; UAVG = 0.0; UU = 0.0;
    ALBMED = 0.0; TRNMED = 0.0; 
  end subroutine allocate_disort_allocatable_arrays

  subroutine deallocate_disort_allocatable_arrays()
    deallocate( DTAUC, SSALB, PMOM, TEMPER, UTAU, UMU, PHI, H_LYR )  
    deallocate( RHOQ, RHOU, EMUST, BEMST, RHO_ACCURATE )                
    deallocate( RFLDIR, RFLDN, FLUP, DFDT, UAVG, ALBMED, TRNMED, UU )  
  end subroutine deallocate_disort_allocatable_arrays
end module disort_variables


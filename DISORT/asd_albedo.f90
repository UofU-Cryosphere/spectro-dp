program disort_albedo
  use f90getopt
  use disort_variables
  implicit none

  ! CLI values
  CHARACTER(len=100) :: ASYM_FILE, SSA_FILE
  integer            :: IO_STATUS

  ! Maximum number of bands to simulate  
  INTEGER :: BANDS=0
  ! Effective size in micro-meter
  INTEGER :: GRAINSIZE=148

  REAL, DIMENSION(:,:), ALLOCATABLE :: ASYMF
  REAL, DIMENSION(:,:), ALLOCATABLE :: SALB
  REAL, DIMENSION(:,:), ALLOCATABLE :: ALBS

  REAL(kind=4),PARAMETER :: PI = 2.*ASIN(1.0)

  INTEGER :: IU, I, J
  CHARACTER  HEADER*127
      
  ! Command line options
  type(option_s):: opts(2)
  opts(1) = option_s( "asymmetry",  .TRUE.,  'a' )
  opts(2) = option_s( "ssa",  .TRUE., 's')

  if (command_argument_count() .NE. 4 ) then
    WRITE (*, *) "Required Options: --asymmetry path_to_file -ssa path_to_file"
    CALL EXIT(-1)
  end if

  ! Process command line options one by one
  do
    select case( getopt( "ash:", opts ) )
      case( char(0) )
        exit
      case( 'a' )
        ASYM_FILE = optarg
      case( 's' )
        SSA_FILE = optarg
      case( 'h' )
    end select
  end do

  ! Get number of lines, equal to bands, from ASYM_FILE
  OPEN(10, file=ASYM_FILE, iostat=IO_STATUS, status='old')
  if (IO_STATUS/=0) STOP 'Cannot open assymetry file'

  BANDS = 0
  do
    READ(10, *, iostat=IO_STATUS)
    if (IO_STATUS/=0) EXIT
    BANDS = BANDS + 1
  end do
  CLOSE(10)

  allocate(ASYMF(GRAINSIZE, BANDS))
  allocate(SALB(GRAINSIZE, BANDS))
  allocate(ALBS(GRAINSIZE, BANDS))

  OPEN(unit=8,file=ASYM_FILE)
  READ(8,*) ASYMF
  CLOSE(8)

  OPEN(unit=10,file=SSA_FILE, iostat=IO_STATUS, status='old')
  if (IO_STATUS/=0) STOP 'Cannot open ssa file'
  READ(10,*) SALB
  CLOSE(10)

  ACCUR = 0.0

  DO I = 1, BANDS
    DO J = 1, GRAINSIZE
      USRTAU    = .FALSE.
      USRANG    = .TRUE.
      LAMBER    = .FALSE.
      PLANK     = .FALSE.
      DO_PSEUDO_SPHERE = .FALSE.
      DELTAMPLUS = .FALSE.

      NSTR = 16; IF(MOD(NSTR,2).NE.0) NSTR = NSTR+1;
      NLYR = 1; 
      NMOM = NSTR 
      NTAU = 4; IF(.NOT.USRTAU) NTAU = NLYR + 1
      !NUMU      = 1; IF(.NOT.USRANG) NUMU = NSTR
      NPHI = 1; 


      IBCND  = 1
      NLYR   = 1; 
      ONLYFL = .FALSE.
      USRANG = .TRUE.      
      NUMU   = 1; IF(.NOT.USRANG) NUMU = NSTR  
  
      IF( USRANG .AND. IBCND.EQ.1 ) THEN
        NUMU_O = NUMU
        NUMU = 2*NUMU
      END IF    
          
      call allocate_disort_allocatable_arrays( NLYR, NMOM, NSTR, NUMU, NPHI, NTAU )

      DTAUC( 1 ) = 1000.0
      SSALB( 1 ) = SALB(J,I)
      CALL  GETMOM( 3, ASYMF(J,I), NMOM, PMOM )
      PRNT( 4 )  = .FALSE.
      PRNT( 2 )  = .FALSE.
      PRNT( 1 )  = .FALSE.
      UMU( 1 )   =  0.9205       

      DO IU = 1, NUMU_O
        UMU( IU + NUMU_O ) = UMU( IU )
      ENDDO  

      DO IU = 1, NUMU_O
        UMU( IU ) = -UMU( 2*NUMU_O + 1 - IU )
      ENDDO    

      ALBEDO = 0.0
      HEADER = ''

      CALL DISORT( NLYR, NMOM, NSTR, NUMU, NPHI, NTAU,           &
               USRANG, USRTAU, IBCND, ONLYFL, PRNT,          &
               PLANK, LAMBER, DELTAMPLUS, DO_PSEUDO_SPHERE,  &          
               DTAUC, SSALB, PMOM, TEMPER, WVNMLO, WVNMHI,   & 
               UTAU, UMU0, PHI0, UMU, PHI, FBEAM,            &                        
               FISOT, ALBEDO, BTEMP, TTEMP, TEMIS,           &
               EARTH_RADIUS, H_LYR,                          &
               RHOQ, RHOU, RHO_ACCURATE, BEMST, EMUST,       &
               ACCUR,  HEADER,                               &
               RFLDIR, RFLDN, FLUP, DFDT, UAVG, UU,          &
               ALBMED, TRNMED )     

      ALBS(J,I) = ALBMED(1)
         
          
      call deallocate_disort_allocatable_arrays()              
    ENDDO
  ENDDO

  deallocate(ASYMF)
  deallocate(SALB)

  ! output file with albedo
  OPEN(unit = 1,file = "albedo.csv")
  DO I = 1, BANDS
    WRITE(1,*) (ALBS(J,I), J=1, GRAINSIZE)
  ENDDO
  CLOSE(1) 

  deallocate(ALBS)

end program disort_albedo

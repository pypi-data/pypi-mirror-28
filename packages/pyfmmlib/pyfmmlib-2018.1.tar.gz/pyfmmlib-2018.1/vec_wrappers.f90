subroutine triangle_norm_vec(triangles, trinorm, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: triangles(3,3,nvcount)
  real*8, intent(out) :: trinorm(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call triangle_norm(triangles(1, 1, ivcount), trinorm(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, triangles,&
    !$omp trinorm)
    do ivcount = 1, nvcount
        call triangle_norm(triangles(1, 1, ivcount), trinorm(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine triangle_area_vec(triangles, triarea, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: triangles(3,3,nvcount)
  real*8, intent(out) :: triarea(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call triangle_area(triangles(1, 1, ivcount), triarea(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, triangles,&
    !$omp triarea)
    do ivcount = 1, nvcount
        call triangle_area(triangles(1, 1, ivcount), triarea(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine ylgndr_vec(nmax, x, y, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: nmax
  real *8, intent(in) :: x(nvcount)
  real *8, intent(out) :: y(0:nmax,0:nmax,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call ylgndr(nmax, x(ivcount), y(0, 0, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, nmax, x, y)
    do ivcount = 1, nvcount
        call ylgndr(nmax, x(ivcount), y(0, 0, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine hank103_vec(z, h0, h1, ifexpon, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: z(nvcount)
  complex*16, intent(out) :: h0(nvcount)
  complex*16, intent(out) :: h1(nvcount)
  integer, intent(in) :: ifexpon

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call hank103(z(ivcount), h0(ivcount), h1(ivcount), ifexpon)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, z, h0, h1,&
    !$omp ifexpon)
    do ivcount = 1, nvcount
        call hank103(z(ivcount), h0(ivcount), h1(ivcount), ifexpon)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine legefder_vec(x, val, der, pexp, n, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: x(nvcount)
  real*8, intent(out) :: val(nvcount)
  real*8, intent(out) :: der(nvcount)
  real*8, intent(in) :: pexp(n+1)
  integer, intent(in) :: n

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call legefder(x(ivcount), val(ivcount), der(ivcount), pexp, n)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, x, val,   &
    !$omp der, pexp, n)
    do ivcount = 1, nvcount
        call legefder(x(ivcount), val(ivcount), der(ivcount), pexp, n)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine lpotgrad2dall_vec(ifgrad, ifhess, sources, charge, nsources,        &
    targets, pot, grad, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: ifgrad
  integer, intent(in) :: ifhess
  real *8, intent(in) :: sources(2,nsources)
  complex *16, intent(in) :: charge(nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(2,nvcount)
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: grad(2,nvcount)
  complex *16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call lpotgrad2dall(ifgrad, ifhess, sources, charge, nsources, targets(1,       &
          ivcount), pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, ifgrad,   &
    !$omp ifhess, sources, charge, nsources, targets, pot, grad, hess)
    do ivcount = 1, nvcount
        call lpotgrad2dall(ifgrad, ifhess, sources, charge, nsources, targets(1,       &
          ivcount), pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine lpotfld3dall_vec(iffld, sources, charge, nsources, targets, pot,    &
    fld, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: iffld
  real *8, intent(in) :: sources(3,nsources)
  complex *16, intent(in) :: charge(nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(3,nvcount)
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: fld(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call lpotfld3dall(iffld, sources, charge, nsources, targets(1, ivcount),       &
          pot(ivcount), fld(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, iffld,    &
    !$omp sources, charge, nsources, targets, pot, fld)
    do ivcount = 1, nvcount
        call lpotfld3dall(iffld, sources, charge, nsources, targets(1, ivcount),       &
          pot(ivcount), fld(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine hpotgrad2dall_vec(ifgrad, ifhess, sources, charge, nsources,        &
    targets, zk, pot, grad, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: ifgrad
  integer, intent(in) :: ifhess
  real *8, intent(in) :: sources(2,nsources)
  complex *16, intent(in) :: charge(nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(2,nvcount)
  complex *16, intent(in) :: zk
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: grad(2,nvcount)
  complex *16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call hpotgrad2dall(ifgrad, ifhess, sources, charge, nsources, targets(1,       &
          ivcount), zk, pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, ifgrad,   &
    !$omp ifhess, sources, charge, nsources, targets, zk, pot, grad, hess)
    do ivcount = 1, nvcount
        call hpotgrad2dall(ifgrad, ifhess, sources, charge, nsources, targets(1,       &
          ivcount), zk, pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine hpotfld3dall_vec(iffld, sources, charge, nsources, targets, zk, pot,&
    fld, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: iffld
  real *8, intent(in) :: sources(3,nsources)
  complex *16, intent(in) :: charge(nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(3,nvcount)
  complex *16, intent(in) :: zk
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: fld(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call hpotfld3dall(iffld, sources, charge, nsources, targets(1, ivcount), zk,   &
          pot(ivcount), fld(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, iffld,    &
    !$omp sources, charge, nsources, targets, zk, pot, fld)
    do ivcount = 1, nvcount
        call hpotfld3dall(iffld, sources, charge, nsources, targets(1, ivcount), zk,   &
          pot(ivcount), fld(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine lpotgrad2dall_dp_vec(ifgrad, ifhess, sources, dipstr, nsources,     &
    targets, pot, grad, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: ifgrad
  integer, intent(in) :: ifhess
  real *8, intent(in) :: sources(2,nsources)
  complex *16, intent(in) :: dipstr(nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(2,nvcount)
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: grad(2,nvcount)
  complex *16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call lpotgrad2dall_dp(ifgrad, ifhess, sources, dipstr, nsources, targets(1,    &
          ivcount), pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, ifgrad,   &
    !$omp ifhess, sources, dipstr, nsources, targets, pot, grad, hess)
    do ivcount = 1, nvcount
        call lpotgrad2dall_dp(ifgrad, ifhess, sources, dipstr, nsources, targets(1,    &
          ivcount), pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine lpotfld3dall_dp_vec(iffld, sources, dipstr, dipvec, nsources,       &
    targets, pot, fld, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: iffld
  real *8, intent(in) :: sources(3,nsources)
  complex *16, intent(in) :: dipstr(nsources)
  real*8, intent(in) :: dipvec(3,nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(3,nvcount)
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: fld(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call lpotfld3dall_dp(iffld, sources, dipstr, dipvec, nsources, targets(1,      &
          ivcount), pot(ivcount), fld(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, iffld,    &
    !$omp sources, dipstr, dipvec, nsources, targets, pot, fld)
    do ivcount = 1, nvcount
        call lpotfld3dall_dp(iffld, sources, dipstr, dipvec, nsources, targets(1,      &
          ivcount), pot(ivcount), fld(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine hpotgrad2dall_dp_vec(ifgrad, ifhess, sources, dipstr, dipvec,       &
    nsources, targets, zk, pot, grad, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: ifgrad
  integer, intent(in) :: ifhess
  real *8, intent(in) :: sources(2,nsources)
  complex *16, intent(in) :: dipstr(nsources)
  real*8, intent(in) :: dipvec(2,nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(2,nvcount)
  complex *16, intent(in) :: zk
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: grad(2,nvcount)
  complex *16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call hpotgrad2dall_dp(ifgrad, ifhess, sources, dipstr, dipvec, nsources,       &
          targets(1, ivcount), zk, pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, ifgrad,   &
    !$omp ifhess, sources, dipstr, dipvec, nsources, targets, zk, pot, grad, hess)
    do ivcount = 1, nvcount
        call hpotgrad2dall_dp(ifgrad, ifhess, sources, dipstr, dipvec, nsources,       &
          targets(1, ivcount), zk, pot(ivcount), grad(1, ivcount), hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine hpotfld3dall_dp_vec(iffld, sources, dipstr, dipvec, nsources,       &
    targets, zk, pot, fld, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer, intent(in) :: iffld
  real *8, intent(in) :: sources(3,nsources)
  complex *16, intent(in) :: dipstr(nsources)
  real*8, intent(in) :: dipvec(3,nsources)
  integer, intent(in) :: nsources
  real *8, intent(in) :: targets(3,nvcount)
  complex *16, intent(in) :: zk
  complex *16, intent(out) :: pot(nvcount)
  complex *16, intent(out) :: fld(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call hpotfld3dall_dp(iffld, sources, dipstr, dipvec, nsources, targets(1,      &
          ivcount), zk, pot(ivcount), fld(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, iffld,    &
    !$omp sources, dipstr, dipvec, nsources, targets, zk, pot, fld)
    do ivcount = 1, nvcount
        call hpotfld3dall_dp(iffld, sources, dipstr, dipvec, nsources, targets(1,      &
          ivcount), zk, pot(ivcount), fld(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dformta_imany(ier, rscale, sources, sources_offsets,              &
    sources_starts, charge, charge_offsets, charge_starts, nsources,           &
    nsources_offsets, nsources_starts, center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(2,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: charge(0:*)
  integer, intent(in) :: charge_offsets(0:*)
  integer, intent(in) :: charge_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(2,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(0:nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(0:nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l2dformta(ier_tmp, rscale(ivcount), sources(1,                            &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, rscale, sources, sources_offsets,&
    !$omp sources_starts, charge, charge_offsets, charge_starts, nsources,         &
    !$omp nsources_offsets, nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l2dformta(ier_tmp, rscale(ivcount), sources(1,                            &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dformta_imany(ier, zk, rscale, sources, sources_offsets,          &
    sources_starts, charge, charge_offsets, charge_starts, nsources,           &
    nsources_offsets, nsources_starts, center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(2,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: charge(0:*)
  integer, intent(in) :: charge_offsets(0:*)
  integer, intent(in) :: charge_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(2,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(-(nterms):nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(-(nterms):nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h2dformta(ier_tmp, zk, rscale(ivcount), sources(1,                        &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(-(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, zk, rscale, sources,             &
    !$omp sources_offsets, sources_starts, charge, charge_offsets, charge_starts,  &
    !$omp nsources, nsources_offsets, nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h2dformta(ier_tmp, zk, rscale(ivcount), sources(1,                        &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(-(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dformta_imany(ier, rscale, sources, sources_offsets,              &
    sources_starts, charge, charge_offsets, charge_starts, nsources,           &
    nsources_offsets, nsources_starts, center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(3,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: charge(0:*)
  integer, intent(in) :: charge_offsets(0:*)
  integer, intent(in) :: charge_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(3,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(0:nterms,-(nterms):nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(0:nterms, -(nterms):nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dformta(ier_tmp, rscale(ivcount), sources(1,                            &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, rscale, sources, sources_offsets,&
    !$omp sources_starts, charge, charge_offsets, charge_starts, nsources,         &
    !$omp nsources_offsets, nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dformta(ier_tmp, rscale(ivcount), sources(1,                            &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dformta_imany(ier, zk, rscale, sources, sources_offsets,          &
    sources_starts, charge, charge_offsets, charge_starts, nsources,           &
    nsources_offsets, nsources_starts, center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(3,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: charge(0:*)
  integer, intent(in) :: charge_offsets(0:*)
  integer, intent(in) :: charge_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(3,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(0:nterms,-(nterms):nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(0:nterms, -(nterms):nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dformta(ier_tmp, zk, rscale(ivcount), sources(1,                        &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, zk, rscale, sources,             &
    !$omp sources_offsets, sources_starts, charge, charge_offsets, charge_starts,  &
    !$omp nsources, nsources_offsets, nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dformta(ier_tmp, zk, rscale(ivcount), sources(1,                        &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          charge(charge_offsets(charge_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dformta_dp_imany(ier, rscale, sources, sources_offsets,           &
    sources_starts, dipstr, dipstr_offsets, dipstr_starts, nsources,           &
    nsources_offsets, nsources_starts, center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(2,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: dipstr(0:*)
  integer, intent(in) :: dipstr_offsets(0:*)
  integer, intent(in) :: dipstr_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(2,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(0:nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(0:nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l2dformta_dp(ier_tmp, rscale(ivcount), sources(1,                         &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, rscale, sources, sources_offsets,&
    !$omp sources_starts, dipstr, dipstr_offsets, dipstr_starts, nsources,         &
    !$omp nsources_offsets, nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l2dformta_dp(ier_tmp, rscale(ivcount), sources(1,                         &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)),                       &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dformta_dp_imany(ier, zk, rscale, sources, sources_offsets,       &
    sources_starts, dipstr, dipstr_offsets, dipstr_starts, dipvec,             &
    dipvec_offsets, dipvec_starts, nsources, nsources_offsets, nsources_starts,&
    center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(2,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: dipstr(0:*)
  integer, intent(in) :: dipstr_offsets(0:*)
  integer, intent(in) :: dipstr_starts(nvcount+1)
  real *8, intent(in) :: dipvec(2,0:*)
  integer, intent(in) :: dipvec_offsets(0:*)
  integer, intent(in) :: dipvec_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(2,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(-(nterms):nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(-(nterms):nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h2dformta_dp(ier_tmp, zk, rscale(ivcount), sources(1,                     &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)), dipvec(1,             &
          dipvec_offsets(dipvec_starts(ivcount) + icsr)),                              &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(-(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, zk, rscale, sources,             &
    !$omp sources_offsets, sources_starts, dipstr, dipstr_offsets, dipstr_starts,  &
    !$omp dipvec, dipvec_offsets, dipvec_starts, nsources, nsources_offsets,       &
    !$omp nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h2dformta_dp(ier_tmp, zk, rscale(ivcount), sources(1,                     &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)), dipvec(1,             &
          dipvec_offsets(dipvec_starts(ivcount) + icsr)),                              &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(-(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, ivcount) = expn(:, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dformta_dp_imany(ier, rscale, sources, sources_offsets,           &
    sources_starts, dipstr, dipstr_offsets, dipstr_starts, dipvec,             &
    dipvec_offsets, dipvec_starts, nsources, nsources_offsets, nsources_starts,&
    center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(3,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: dipstr(0:*)
  integer, intent(in) :: dipstr_offsets(0:*)
  integer, intent(in) :: dipstr_starts(nvcount+1)
  real *8, intent(in) :: dipvec(3,0:*)
  integer, intent(in) :: dipvec_offsets(0:*)
  integer, intent(in) :: dipvec_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(3,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(0:nterms,-(nterms):nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(0:nterms, -(nterms):nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dformta_dp(ier_tmp, rscale(ivcount), sources(1,                         &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)), dipvec(1,             &
          dipvec_offsets(dipvec_starts(ivcount) + icsr)),                              &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, rscale, sources, sources_offsets,&
    !$omp sources_starts, dipstr, dipstr_offsets, dipstr_starts, dipvec,           &
    !$omp dipvec_offsets, dipvec_starts, nsources, nsources_offsets,               &
    !$omp nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dformta_dp(ier_tmp, rscale(ivcount), sources(1,                         &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)), dipvec(1,             &
          dipvec_offsets(dipvec_starts(ivcount) + icsr)),                              &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dformta_dp_imany(ier, zk, rscale, sources, sources_offsets,       &
    sources_starts, dipstr, dipstr_offsets, dipstr_starts, dipvec,             &
    dipvec_offsets, dipvec_starts, nsources, nsources_offsets, nsources_starts,&
    center, nterms, expn, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale(nvcount)
  real *8, intent(in) :: sources(3,0:*)
  integer, intent(in) :: sources_offsets(0:*)
  integer, intent(in) :: sources_starts(nvcount+1)
  complex *16, intent(in) :: dipstr(0:*)
  integer, intent(in) :: dipstr_offsets(0:*)
  integer, intent(in) :: dipstr_starts(nvcount+1)
  real *8, intent(in) :: dipvec(3,0:*)
  integer, intent(in) :: dipvec_offsets(0:*)
  integer, intent(in) :: dipvec_starts(nvcount+1)
  integer, intent(in) :: nsources(0:*)
  integer, intent(in) :: nsources_offsets(0:*)
  integer, intent(in) :: nsources_starts(nvcount+1)
  real*8, intent(in) :: center(3,nvcount)
  integer, intent(in) :: nterms
  complex*16 expn(0:nterms,-(nterms):nterms,nvcount)
  !f2py intent(in,out) expn
  complex*16 :: expn_tmp(0:nterms, -(nterms):nterms)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dformta_dp(ier_tmp, zk, rscale(ivcount), sources(1,                     &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)), dipvec(1,             &
          dipvec_offsets(dipvec_starts(ivcount) + icsr)),                              &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp ier_tmp, expn_tmp) shared(nvcount, ier, zk, rscale, sources,             &
    !$omp sources_offsets, sources_starts, dipstr, dipstr_offsets, dipstr_starts,  &
    !$omp dipvec, dipvec_offsets, dipvec_starts, nsources, nsources_offsets,       &
    !$omp nsources_starts, center, nterms, expn)
    do ivcount = 1, nvcount
      ncsr_count = sources_starts(ivcount+1) - sources_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dformta_dp(ier_tmp, zk, rscale(ivcount), sources(1,                     &
          sources_offsets(sources_starts(ivcount) + icsr)),                            &
          dipstr(dipstr_offsets(dipstr_starts(ivcount) + icsr)), dipvec(1,             &
          dipvec_offsets(dipvec_starts(ivcount) + icsr)),                              &
          nsources(nsources_offsets(nsources_starts(ivcount) + icsr)), center(1,       &
          ivcount), nterms, expn_tmp(0, -(nterms)))
        ier(ivcount) = max(ier(ivcount), ier_tmp)
        expn(:, :, ivcount) = expn(:, :, ivcount) + expn_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end




                    subroutine l2dformta_qbx( &
                            ier,  &
                            nsources, sources, &
                            charge, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(2, 0:nsources-1)
                            complex *16, intent(in) :: charge(0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 2)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                0:nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(2)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(0:nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,   &
                        !$omp   nsources, sources, &
                        !$omp           charge, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(0:nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call l2dformta( &
                                    ier_tmp,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        charge(isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(0:nterms, tgt_icenter) = &
                                    expn(0:nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end




                    subroutine h2dformta_qbx( &
                            ier, zk,  &
                            nsources, sources, &
                            charge, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier

                complex*16, intent(in) :: zk


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(2, 0:nsources-1)
                            complex *16, intent(in) :: charge(0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 2)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                -(nterms):nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(2)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(-(nterms):nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,  zk,  &
                        !$omp   nsources, sources, &
                        !$omp           charge, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(-(nterms):nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call h2dformta( &
                                    ier_tmp, zk,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        charge(isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(-(nterms):nterms, tgt_icenter) = &
                                    expn(-(nterms):nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end




                    subroutine l3dformta_qbx( &
                            ier,  &
                            nsources, sources, &
                            charge, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(3, 0:nsources-1)
                            complex *16, intent(in) :: charge(0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 3)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                0:nterms,-(nterms):nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(3)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(0:nterms,-(nterms):nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,   &
                        !$omp   nsources, sources, &
                        !$omp           charge, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(0:nterms,-(nterms):nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call l3dformta( &
                                    ier_tmp,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        charge(isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(0:nterms,-(nterms):nterms, tgt_icenter) = &
                                    expn(0:nterms,-(nterms):nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end




                    subroutine h3dformta_qbx( &
                            ier, zk,  &
                            nsources, sources, &
                            charge, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier

                complex*16, intent(in) :: zk


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(3, 0:nsources-1)
                            complex *16, intent(in) :: charge(0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 3)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                0:nterms,-(nterms):nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(3)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(0:nterms,-(nterms):nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,  zk,  &
                        !$omp   nsources, sources, &
                        !$omp           charge, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(0:nterms,-(nterms):nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call h3dformta( &
                                    ier_tmp, zk,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        charge(isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(0:nterms,-(nterms):nterms, tgt_icenter) = &
                                    expn(0:nterms,-(nterms):nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end




                    subroutine l2dformta_dp_qbx( &
                            ier,  &
                            nsources, sources, &
                            dipstr, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(2, 0:nsources-1)
                            complex *16, intent(in) :: dipstr(0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 2)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                0:nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(2)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(0:nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,   &
                        !$omp   nsources, sources, &
                        !$omp           dipstr, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(0:nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call l2dformta_dp( &
                                    ier_tmp,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        dipstr(isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(0:nterms, tgt_icenter) = &
                                    expn(0:nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end




                    subroutine h2dformta_dp_qbx( &
                            ier, zk,  &
                            nsources, sources, &
                            dipstr, dipvec, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier

                complex*16, intent(in) :: zk


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(2, 0:nsources-1)
                            complex *16, intent(in) :: dipstr(0:*)
                                real *8, intent(in) :: dipvec(2, 0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 2)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                -(nterms):nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(2)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(-(nterms):nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,  zk,  &
                        !$omp   nsources, sources, &
                        !$omp           dipstr, &
                        !$omp               dipvec, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(-(nterms):nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call h2dformta_dp( &
                                    ier_tmp, zk,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        dipstr(isrc_start), &
                                            dipvec(1, isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(-(nterms):nterms, tgt_icenter) = &
                                    expn(-(nterms):nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end




                    subroutine l3dformta_dp_qbx( &
                            ier,  &
                            nsources, sources, &
                            dipstr, dipvec, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(3, 0:nsources-1)
                            complex *16, intent(in) :: dipstr(0:*)
                                real *8, intent(in) :: dipvec(3, 0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 3)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                0:nterms,-(nterms):nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(3)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(0:nterms,-(nterms):nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,   &
                        !$omp   nsources, sources, &
                        !$omp           dipstr, &
                        !$omp               dipvec, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(0:nterms,-(nterms):nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call l3dformta_dp( &
                                    ier_tmp,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        dipstr(isrc_start), &
                                            dipvec(1, isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(0:nterms,-(nterms):nterms, tgt_icenter) = &
                                    expn(0:nterms,-(nterms):nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end




                    subroutine h3dformta_dp_qbx( &
                            ier, zk,  &
                            nsources, sources, &
                            dipstr, dipvec, &
                            ntgt_centers, nqbx_centers, qbx_centers, &
                            global_qbx_centers, &
                            qbx_expansion_radii, &
                            qbx_center_to_target_box, &
                            nterms, &
                            source_box_starts, source_box_lists, &
                            box_source_starts, box_source_counts_nonchild, &
                            expn &
                            )
                        implicit none

                        ! ------------------ arguments

                        integer, intent(out) :: ier

                complex*16, intent(in) :: zk


                        integer, intent(in) :: nsources
                        real *8, intent(in) :: sources(3, 0:nsources-1)
                            complex *16, intent(in) :: dipstr(0:*)
                                real *8, intent(in) :: dipvec(3, 0:*)
                        integer, intent(in) :: ntgt_centers
                        integer, intent(in) :: nqbx_centers
                        integer, intent(in) :: global_qbx_centers(0:ntgt_centers-1)
                        real*8, intent(in) :: qbx_centers(0:nqbx_centers-1, 3)
                        real*8, intent(in) :: qbx_expansion_radii(0:nqbx_centers-1)
                        integer, intent(in) :: qbx_center_to_target_box( &
                            0:nqbx_centers-1)
                        integer, intent(in) :: nterms

                        integer, intent(in) :: source_box_starts(0:*)
                        integer, intent(in) :: source_box_lists(0:*)

                        integer, intent(in) :: box_source_starts(0:*)
                        integer, intent(in) :: box_source_counts_nonchild(0:*)

                        complex*16, intent(out) :: expn( &
                                0:nterms,-(nterms):nterms, &
                                0:nqbx_centers-1)

                        ! ------------------ local vars

                        integer itgt_center
                        integer tgt_icenter

                        integer itgt_box
                        real*8 rscale
                        real*8 center(3)

                        integer isrc_box, isrc_box_start, isrc_box_stop

                        integer src_ibox
                        integer isrc_start

                        integer ier_tmp
                        complex*16 expn_tmp(0:nterms,-(nterms):nterms)

                        ! ------------------ code

                        ier = 0

                        !$omp parallel do default(none) schedule(dynamic, 10) &
                        !$omp private(tgt_icenter, center, rscale, itgt_box, &
                        !$omp   isrc_box_start, isrc_box_stop, src_ibox, &
                        !$omp   isrc_start, expn_tmp, ier_tmp) &
                        !$omp shared(ier,  zk,  &
                        !$omp   nsources, sources, &
                        !$omp           dipstr, &
                        !$omp               dipvec, &
                        !$omp   ntgt_centers, nqbx_centers, &
                        !$omp   global_qbx_centers, qbx_centers, &
                        !$omp   qbx_expansion_radii, &
                        !$omp   qbx_center_to_target_box, nterms, &
                        !$omp   source_box_starts, source_box_lists, &
                        !$omp   box_source_starts, box_source_counts_nonchild, expn)

                        do itgt_center = 0, ntgt_centers-1
                            tgt_icenter = global_qbx_centers(itgt_center)

                            expn(0:nterms,-(nterms):nterms, tgt_icenter) = 0

                            center = qbx_centers(tgt_icenter, :)
                            rscale = qbx_expansion_radii(tgt_icenter)

                            itgt_box = qbx_center_to_target_box(tgt_icenter)

                            isrc_box_start = source_box_starts(itgt_box)
                            isrc_box_stop = source_box_starts(itgt_box+1)

                            do isrc_box = isrc_box_start, isrc_box_stop-1
                                src_ibox = source_box_lists(isrc_box)
                                isrc_start = box_source_starts(src_ibox)

                                ier_tmp = 0
                                call h3dformta_dp( &
                                    ier_tmp, zk,  &
                                    rscale, &
                                    sources(1, isrc_start), &
                                        dipstr(isrc_start), &
                                            dipvec(1, isrc_start), &
                                    box_source_counts_nonchild(src_ibox), &
                                    center, &
                                    nterms, &
                                    expn_tmp)

                                expn(0:nterms,-(nterms):nterms, tgt_icenter) = &
                                    expn(0:nterms,-(nterms):nterms, tgt_icenter) + expn_tmp

                                if (ier_tmp.ne.0) then
                                    ier = ier_tmp
                                end if
                            end do
                        end do
                    end

subroutine l3dtaeval_vec(rscale, center, expn, nterms, ztarg, pot, iffld, fld, &
    ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(3)
  complex*16, intent(in) :: expn(0:nterms,-nterms:nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(3,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: iffld
  complex*16, intent(out) :: fld(3,nvcount)
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l3dtaeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          iffld, fld(1, ivcount), ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale,   &
    !$omp center, expn, nterms, ztarg, pot, iffld, fld, ier)
    do ivcount = 1, nvcount
        call l3dtaeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          iffld, fld(1, ivcount), ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dmpeval_vec(rscale, center, expn, nterms, ztarg, pot, iffld, fld, &
    ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(3)
  complex*16, intent(in) :: expn(0:nterms,-nterms:nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(3,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: iffld
  complex*16, intent(out) :: fld(3,nvcount)
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l3dmpeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          iffld, fld(1, ivcount), ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale,   &
    !$omp center, expn, nterms, ztarg, pot, iffld, fld, ier)
    do ivcount = 1, nvcount
        call l3dmpeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          iffld, fld(1, ivcount), ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dtaeval_vec(zk, rscale, center, expn, nterms, ztarg, pot, iffld,  &
    fld, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(3)
  complex*16, intent(in) :: expn(0:nterms,-nterms:nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(3,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: iffld
  complex*16, intent(out) :: fld(3,nvcount)
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h3dtaeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), iffld, fld(1, ivcount), ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale, center, expn, nterms, ztarg, pot, iffld, fld, ier)
    do ivcount = 1, nvcount
        call h3dtaeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), iffld, fld(1, ivcount), ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dmpeval_vec(zk, rscale, center, expn, nterms, ztarg, pot, iffld,  &
    fld, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(3)
  complex*16, intent(in) :: expn(0:nterms,-nterms:nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(3,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: iffld
  complex*16, intent(out) :: fld(3,nvcount)
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h3dmpeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), iffld, fld(1, ivcount), ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale, center, expn, nterms, ztarg, pot, iffld, fld, ier)
    do ivcount = 1, nvcount
        call h3dmpeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), iffld, fld(1, ivcount), ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dtaeval_vec(rscale, center, expn, nterms, ztarg, pot, ifgrad,     &
    grad, ifhess, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(2)
  complex*16, intent(in) :: expn(0:nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(2,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: ifgrad
  complex*16, intent(out) :: grad(2,nvcount)
  integer, intent(in) :: ifhess
  complex*16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l2dtaeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale,   &
    !$omp center, expn, nterms, ztarg, pot, ifgrad, grad, ifhess, hess)
    do ivcount = 1, nvcount
        call l2dtaeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dmpeval_vec(rscale, center, expn, nterms, ztarg, pot, ifgrad,     &
    grad, ifhess, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(2)
  complex*16, intent(in) :: expn(0:nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(2,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: ifgrad
  complex*16, intent(out) :: grad(2,nvcount)
  integer, intent(in) :: ifhess
  complex*16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l2dmpeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale,   &
    !$omp center, expn, nterms, ztarg, pot, ifgrad, grad, ifhess, hess)
    do ivcount = 1, nvcount
        call l2dmpeval(rscale, center, expn, nterms, ztarg(1, ivcount), pot(ivcount),  &
          ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dtaeval_vec(zk, rscale, center, expn, nterms, ztarg, pot, ifgrad, &
    grad, ifhess, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(2)
  complex*16, intent(in) :: expn(-(nterms):nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(2,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: ifgrad
  complex*16, intent(out) :: grad(2,nvcount)
  integer, intent(in) :: ifhess
  complex*16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h2dtaeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale, center, expn, nterms, ztarg, pot, ifgrad, grad, ifhess, hess)
    do ivcount = 1, nvcount
        call h2dtaeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dmpeval_vec(zk, rscale, center, expn, nterms, ztarg, pot, ifgrad, &
    grad, ifhess, hess, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale
  real*8, intent(in) :: center(2)
  complex*16, intent(in) :: expn(-(nterms):nterms)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(2,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: ifgrad
  complex*16, intent(out) :: grad(2,nvcount)
  integer, intent(in) :: ifhess
  complex*16, intent(out) :: hess(3,nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h2dmpeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale, center, expn, nterms, ztarg, pot, ifgrad, grad, ifhess, hess)
    do ivcount = 1, nvcount
        call h2dmpeval(zk, rscale, center, expn, nterms, ztarg(1, ivcount),            &
          pot(ivcount), ifgrad, grad(1, ivcount), ifhess, hess(1, ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dtaevalhess_1tgtperexp(rscale, center, expn, nterms, ztarg, pot,  &
    ifgrad, grad, ifhess, hess, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale(nvcount)
  real*8, intent(in) :: center(3,nvcount)
  complex *16, intent(in) :: expn(0:nterms,-nterms:nterms,nvcount)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(3,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: ifgrad
  complex*16, intent(out) :: grad(3,nvcount)
  integer, intent(in) :: ifhess
  complex*16, intent(out) :: hess(6,nvcount)
  integer, intent(out) :: ier

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l3dtaevalhess(rscale(ivcount), center(1, ivcount), expn(0, -nterms,       &
          ivcount), nterms, ztarg(1, ivcount), pot(ivcount), ifgrad, grad(1, ivcount), &
          ifhess, hess(1, ivcount), ier)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale,   &
    !$omp center, expn, nterms, ztarg, pot, ifgrad, grad, ifhess, hess, ier)
    do ivcount = 1, nvcount
        call l3dtaevalhess(rscale(ivcount), center(1, ivcount), expn(0, -nterms,       &
          ivcount), nterms, ztarg(1, ivcount), pot(ivcount), ifgrad, grad(1, ivcount), &
          ifhess, hess(1, ivcount), ier)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dtaeval_1tgtperexp(zk, rscale, center, expn, nterms, ztarg, pot,  &
    ifgrad, grad, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale(nvcount)
  real*8, intent(in) :: center(3,nvcount)
  complex *16, intent(in) :: expn(0:nterms,-nterms:nterms,nvcount)
  integer, intent(in) :: nterms
  real*8, intent(in) :: ztarg(3,nvcount)
  complex*16, intent(out) :: pot(nvcount)
  integer, intent(in) :: ifgrad
  complex*16, intent(out) :: grad(3,nvcount)
  integer, intent(out) :: ier

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h3dtaeval(zk, rscale(ivcount), center(1, ivcount), expn(0, -nterms,       &
          ivcount), nterms, ztarg(1, ivcount), pot(ivcount), ifgrad, grad(1, ivcount), &
          ier)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale, center, expn, nterms, ztarg, pot, ifgrad, grad, ier)
    do ivcount = 1, nvcount
        call h3dtaeval(zk, rscale(ivcount), center(1, ivcount), expn(0, -nterms,       &
          ivcount), nterms, ztarg(1, ivcount), pot(ivcount), ifgrad, grad(1, ivcount), &
          ier)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dmpmp_vec(rscale1, center1, expn1, nterms1, rscale2, center2,     &
    expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(2,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,nvcount)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l2dmpmp(rscale1(ivcount), center1(1, ivcount), expn1(0, ivcount), nterms1,&
          rscale2(ivcount), center2(1, ivcount), expn2(0, ivcount), nterms2)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale1,  &
    !$omp center1, expn1, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
        call l2dmpmp(rscale1(ivcount), center1(1, ivcount), expn1(0, ivcount), nterms1,&
          rscale2(ivcount), center2(1, ivcount), expn2(0, ivcount), nterms2)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dmpmp_imany(rscale1, rscale1_offsets, rscale1_starts, center1,    &
    center1_offsets, center1_starts, expn1, expn1_offsets, expn1_starts,       &
    nterms1, rscale2, center2, expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(2,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16 expn2(0:nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call l2dmpmp(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),         &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1, rscale2(ivcount),     &
          center2(1, ivcount), expn2_tmp(0), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp) shared(nvcount, rscale1, rscale1_offsets, rscale1_starts,     &
    !$omp center1, center1_offsets, center1_starts, expn1, expn1_offsets,          &
    !$omp expn1_starts, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call l2dmpmp(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),         &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1, rscale2(ivcount),     &
          center2(1, ivcount), expn2_tmp(0), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dmploc_vec(rscale1, center1, expn1, nterms1, rscale2, center2,    &
    expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(2,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,nvcount)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l2dmploc(rscale1(ivcount), center1(1, ivcount), expn1(0, ivcount),        &
          nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0, ivcount), nterms2)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale1,  &
    !$omp center1, expn1, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
        call l2dmploc(rscale1(ivcount), center1(1, ivcount), expn1(0, ivcount),        &
          nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0, ivcount), nterms2)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dmploc_imany(rscale1, rscale1_offsets, rscale1_starts, center1,   &
    center1_offsets, center1_starts, expn1, expn1_offsets, expn1_starts,       &
    nterms1, rscale2, center2, expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(2,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16 expn2(0:nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call l2dmploc(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),        &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1, rscale2(ivcount),     &
          center2(1, ivcount), expn2_tmp(0), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp) shared(nvcount, rscale1, rscale1_offsets, rscale1_starts,     &
    !$omp center1, center1_offsets, center1_starts, expn1, expn1_offsets,          &
    !$omp expn1_starts, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call l2dmploc(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),        &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1, rscale2(ivcount),     &
          center2(1, ivcount), expn2_tmp(0), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dlocloc_vec(rscale1, center1, expn1, nterms1, rscale2, center2,   &
    expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(2,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,nvcount)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l2dlocloc(rscale1(ivcount), center1(1, ivcount), expn1(0, ivcount),       &
          nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0, ivcount), nterms2)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale1,  &
    !$omp center1, expn1, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
        call l2dlocloc(rscale1(ivcount), center1(1, ivcount), expn1(0, ivcount),       &
          nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0, ivcount), nterms2)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l2dlocloc_imany(rscale1, rscale1_offsets, rscale1_starts, center1,  &
    center1_offsets, center1_starts, expn1, expn1_offsets, expn1_starts,       &
    nterms1, rscale2, center2, expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(2,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16 expn2(0:nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call l2dlocloc(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),       &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1, rscale2(ivcount),     &
          center2(1, ivcount), expn2_tmp(0), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp) shared(nvcount, rscale1, rscale1_offsets, rscale1_starts,     &
    !$omp center1, center1_offsets, center1_starts, expn1, expn1_offsets,          &
    !$omp expn1_starts, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call l2dlocloc(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),       &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1, rscale2(ivcount),     &
          center2(1, ivcount), expn2_tmp(0), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dmpmp_vec(zk, rscale1, center1, expn1, nterms1, rscale2, center2, &
    expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(2,nvcount)
  complex*16, intent(in) :: expn1(-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16, intent(out) :: expn2(-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h2dmpmp(zk, rscale1(ivcount), center1(1, ivcount), expn1(-(nterms1),      &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(-(nterms2),  &
          ivcount), nterms2)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale1, center1, expn1, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
        call h2dmpmp(zk, rscale1(ivcount), center1(1, ivcount), expn1(-(nterms1),      &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(-(nterms2),  &
          ivcount), nterms2)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dmpmp_imany(zk, rscale1, rscale1_offsets, rscale1_starts, center1,&
    center1_offsets, center1_starts, expn1, expn1_offsets, expn1_starts,       &
    nterms1, rscale2, center2, expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(2,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16 expn2(-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(-(nterms2):nterms2)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call h2dmpmp(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),     &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)),                 &
          expn1(-(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,     &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(-(nterms2)), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp) shared(nvcount, zk, rscale1, rscale1_offsets, rscale1_starts, &
    !$omp center1, center1_offsets, center1_starts, expn1, expn1_offsets,          &
    !$omp expn1_starts, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call h2dmpmp(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),     &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)),                 &
          expn1(-(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,     &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(-(nterms2)), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dmploc_vec(zk, rscale1, center1, expn1, nterms1, rscale2, center2,&
    expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(2,nvcount)
  complex*16, intent(in) :: expn1(-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16, intent(out) :: expn2(-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h2dmploc(zk, rscale1(ivcount), center1(1, ivcount), expn1(-(nterms1),     &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(-(nterms2),  &
          ivcount), nterms2)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale1, center1, expn1, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
        call h2dmploc(zk, rscale1(ivcount), center1(1, ivcount), expn1(-(nterms1),     &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(-(nterms2),  &
          ivcount), nterms2)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dmploc_imany(zk, rscale1, rscale1_offsets, rscale1_starts,        &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(2,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16 expn2(-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(-(nterms2):nterms2)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call h2dmploc(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),    &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)),                 &
          expn1(-(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,     &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(-(nterms2)), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp) shared(nvcount, zk, rscale1, rscale1_offsets, rscale1_starts, &
    !$omp center1, center1_offsets, center1_starts, expn1, expn1_offsets,          &
    !$omp expn1_starts, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call h2dmploc(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),    &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)),                 &
          expn1(-(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,     &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(-(nterms2)), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dlocloc_vec(zk, rscale1, center1, expn1, nterms1, rscale2,        &
    center2, expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(2,nvcount)
  complex*16, intent(in) :: expn1(-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16, intent(out) :: expn2(-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h2dlocloc(zk, rscale1(ivcount), center1(1, ivcount), expn1(-(nterms1),    &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(-(nterms2),  &
          ivcount), nterms2)
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale1, center1, expn1, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
        call h2dlocloc(zk, rscale1(ivcount), center1(1, ivcount), expn1(-(nterms1),    &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(-(nterms2),  &
          ivcount), nterms2)
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h2dlocloc_imany(zk, rscale1, rscale1_offsets, rscale1_starts,       &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(2,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(2,nvcount)
  complex*16 expn2(-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(-(nterms2):nterms2)
  integer, intent(in) :: nterms2

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call h2dlocloc(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),   &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)),                 &
          expn1(-(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,     &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(-(nterms2)), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp) shared(nvcount, zk, rscale1, rscale1_offsets, rscale1_starts, &
    !$omp center1, center1_offsets, center1_starts, expn1, expn1_offsets,          &
    !$omp expn1_starts, nterms1, rscale2, center2, expn2, nterms2)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        call h2dlocloc(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),   &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)),                 &
          expn1(-(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,     &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(-(nterms2)), nterms2)
        expn2(:, ivcount) = expn2(:, ivcount) + expn2_tmp
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dmpmpquadu_vec(rscale1, center1, expn1, nterms1, rscale2, center2,&
    expn2, nterms2, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(3,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l3dmpmpquadu(rscale1(ivcount), center1(1, ivcount), expn1(0, -(nterms1),  &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0,           &
          -(nterms2), ivcount), nterms2, ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale1,  &
    !$omp center1, expn1, nterms1, rscale2, center2, expn2, nterms2, ier)
    do ivcount = 1, nvcount
        call l3dmpmpquadu(rscale1(ivcount), center1(1, ivcount), expn1(0, -(nterms1),  &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0,           &
          -(nterms2), ivcount), nterms2, ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dmpmpquadu_imany(rscale1, rscale1_offsets, rscale1_starts,        &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(3,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16 expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2, -(nterms2):nterms2)
  integer, intent(in) :: nterms2
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dmpmpquadu(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),    &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp, ier_tmp) shared(nvcount, rscale1, rscale1_offsets,            &
    !$omp rscale1_starts, center1, center1_offsets, center1_starts, expn1,         &
    !$omp expn1_offsets, expn1_starts, nterms1, rscale2, center2, expn2, nterms2,  &
    !$omp ier)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dmpmpquadu(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),    &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dmplocquadu_vec(rscale1, center1, expn1, nterms1, rscale2,        &
    center2, expn2, nterms2, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(3,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l3dmplocquadu(rscale1(ivcount), center1(1, ivcount), expn1(0, -(nterms1), &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0,           &
          -(nterms2), ivcount), nterms2, ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale1,  &
    !$omp center1, expn1, nterms1, rscale2, center2, expn2, nterms2, ier)
    do ivcount = 1, nvcount
        call l3dmplocquadu(rscale1(ivcount), center1(1, ivcount), expn1(0, -(nterms1), &
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0,           &
          -(nterms2), ivcount), nterms2, ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dmplocquadu_imany(rscale1, rscale1_offsets, rscale1_starts,       &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(3,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16 expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2, -(nterms2):nterms2)
  integer, intent(in) :: nterms2
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dmplocquadu(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),   &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp, ier_tmp) shared(nvcount, rscale1, rscale1_offsets,            &
    !$omp rscale1_starts, center1, center1_offsets, center1_starts, expn1,         &
    !$omp expn1_offsets, expn1_starts, nterms1, rscale2, center2, expn2, nterms2,  &
    !$omp ier)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dmplocquadu(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),   &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dloclocquadu_vec(rscale1, center1, expn1, nterms1, rscale2,       &
    center2, expn2, nterms2, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(3,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call l3dloclocquadu(rscale1(ivcount), center1(1, ivcount), expn1(0, -(nterms1),&
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0,           &
          -(nterms2), ivcount), nterms2, ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, rscale1,  &
    !$omp center1, expn1, nterms1, rscale2, center2, expn2, nterms2, ier)
    do ivcount = 1, nvcount
        call l3dloclocquadu(rscale1(ivcount), center1(1, ivcount), expn1(0, -(nterms1),&
          ivcount), nterms1, rscale2(ivcount), center2(1, ivcount), expn2(0,           &
          -(nterms2), ivcount), nterms2, ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine l3dloclocquadu_imany(rscale1, rscale1_offsets, rscale1_starts,      &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(3,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16 expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2, -(nterms2):nterms2)
  integer, intent(in) :: nterms2
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dloclocquadu(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),  &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp, ier_tmp) shared(nvcount, rscale1, rscale1_offsets,            &
    !$omp rscale1_starts, center1, center1_offsets, center1_starts, expn1,         &
    !$omp expn1_offsets, expn1_starts, nterms1, rscale2, center2, expn2, nterms2,  &
    !$omp ier)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call l3dloclocquadu(rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),  &
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dmpmpquadu_vec(zk, rscale1, center1, expn1, nterms1, rscale2,     &
    center2, expn2, nterms2, radius, xnodes, wts, nquad, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(3,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2
  real*8, intent(in) :: radius(nvcount)
  real*8, intent(in) :: xnodes(nquad)
  real*8, intent(in) :: wts(nquad)
  integer, intent(in) :: nquad
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h3dmpmpquadu(zk, rscale1(ivcount), center1(1, ivcount), expn1(0,          &
          -(nterms1), ivcount), nterms1, rscale2(ivcount), center2(1, ivcount),        &
          expn2(0, -(nterms2), ivcount), nterms2, radius(ivcount), xnodes, wts, nquad, &
          ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale1, center1, expn1, nterms1, rscale2, center2, expn2, nterms2,      &
    !$omp radius, xnodes, wts, nquad, ier)
    do ivcount = 1, nvcount
        call h3dmpmpquadu(zk, rscale1(ivcount), center1(1, ivcount), expn1(0,          &
          -(nterms1), ivcount), nterms1, rscale2(ivcount), center2(1, ivcount),        &
          expn2(0, -(nterms2), ivcount), nterms2, radius(ivcount), xnodes, wts, nquad, &
          ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dmpmpquadu_imany(zk, rscale1, rscale1_offsets, rscale1_starts,    &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, radius, xnodes,   &
    wts, nquad, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(3,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16 expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2, -(nterms2):nterms2)
  integer, intent(in) :: nterms2
  real*8, intent(in) :: radius(nvcount)
  real*8, intent(in) :: xnodes(nquad)
  real*8, intent(in) :: wts(nquad)
  integer, intent(in) :: nquad
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dmpmpquadu(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),&
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          radius(ivcount), xnodes, wts, nquad, ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp, ier_tmp) shared(nvcount, zk, rscale1, rscale1_offsets,        &
    !$omp rscale1_starts, center1, center1_offsets, center1_starts, expn1,         &
    !$omp expn1_offsets, expn1_starts, nterms1, rscale2, center2, expn2, nterms2,  &
    !$omp radius, xnodes, wts, nquad, ier)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dmpmpquadu(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) + icsr)),&
          center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,        &
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          radius(ivcount), xnodes, wts, nquad, ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dmplocquadu_vec(zk, rscale1, center1, expn1, nterms1, rscale2,    &
    center2, expn2, nterms2, radius, xnodes, wts, nquad, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(3,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2
  real*8, intent(in) :: radius(nvcount)
  real*8, intent(in) :: xnodes(nquad)
  real*8, intent(in) :: wts(nquad)
  integer, intent(in) :: nquad
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h3dmplocquadu(zk, rscale1(ivcount), center1(1, ivcount), expn1(0,         &
          -(nterms1), ivcount), nterms1, rscale2(ivcount), center2(1, ivcount),        &
          expn2(0, -(nterms2), ivcount), nterms2, radius(ivcount), xnodes, wts, nquad, &
          ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale1, center1, expn1, nterms1, rscale2, center2, expn2, nterms2,      &
    !$omp radius, xnodes, wts, nquad, ier)
    do ivcount = 1, nvcount
        call h3dmplocquadu(zk, rscale1(ivcount), center1(1, ivcount), expn1(0,         &
          -(nterms1), ivcount), nterms1, rscale2(ivcount), center2(1, ivcount),        &
          expn2(0, -(nterms2), ivcount), nterms2, radius(ivcount), xnodes, wts, nquad, &
          ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dmplocquadu_imany(zk, rscale1, rscale1_offsets, rscale1_starts,   &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, radius, xnodes,   &
    wts, nquad, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(3,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16 expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2, -(nterms2):nterms2)
  integer, intent(in) :: nterms2
  real*8, intent(in) :: radius(nvcount)
  real*8, intent(in) :: xnodes(nquad)
  real*8, intent(in) :: wts(nquad)
  integer, intent(in) :: nquad
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dmplocquadu(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) +       &
          icsr)), center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,&
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          radius(ivcount), xnodes, wts, nquad, ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp, ier_tmp) shared(nvcount, zk, rscale1, rscale1_offsets,        &
    !$omp rscale1_starts, center1, center1_offsets, center1_starts, expn1,         &
    !$omp expn1_offsets, expn1_starts, nterms1, rscale2, center2, expn2, nterms2,  &
    !$omp radius, xnodes, wts, nquad, ier)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dmplocquadu(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) +       &
          icsr)), center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,&
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          radius(ivcount), xnodes, wts, nquad, ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dloclocquadu_vec(zk, rscale1, center1, expn1, nterms1, rscale2,   &
    center2, expn2, nterms2, radius, xnodes, wts, nquad, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(nvcount)
  real*8, intent(in) :: center1(3,nvcount)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,nvcount)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16, intent(out) :: expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  integer, intent(in) :: nterms2
  real*8, intent(in) :: radius(nvcount)
  real*8, intent(in) :: xnodes(nquad)
  real*8, intent(in) :: wts(nquad)
  integer, intent(in) :: nquad
  integer, intent(out) :: ier(nvcount)

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
        call h3dloclocquadu(zk, rscale1(ivcount), center1(1, ivcount), expn1(0,        &
          -(nterms1), ivcount), nterms1, rscale2(ivcount), center2(1, ivcount),        &
          expn2(0, -(nterms2), ivcount), nterms2, radius(ivcount), xnodes, wts, nquad, &
          ier(ivcount))
    enddo
  else
    !$omp parallel do default(none) schedule(static, 10) shared(nvcount, zk,       &
    !$omp rscale1, center1, expn1, nterms1, rscale2, center2, expn2, nterms2,      &
    !$omp radius, xnodes, wts, nquad, ier)
    do ivcount = 1, nvcount
        call h3dloclocquadu(zk, rscale1(ivcount), center1(1, ivcount), expn1(0,        &
          -(nterms1), ivcount), nterms1, rscale2(ivcount), center2(1, ivcount),        &
          expn2(0, -(nterms2), ivcount), nterms2, radius(ivcount), xnodes, wts, nquad, &
          ier(ivcount))
    enddo
    !$omp end parallel do
  endif
  return
end

subroutine h3dloclocquadu_imany(zk, rscale1, rscale1_offsets, rscale1_starts,  &
    center1, center1_offsets, center1_starts, expn1, expn1_offsets,            &
    expn1_starts, nterms1, rscale2, center2, expn2, nterms2, radius, xnodes,   &
    wts, nquad, ier, nvcount)
  implicit none
  integer, intent(in) :: nvcount
  integer ivcount
  integer ncsr_count
  integer icsr
  complex*16, intent(in) :: zk
  real*8, intent(in) :: rscale1(0:*)
  integer, intent(in) :: rscale1_offsets(0:*)
  integer, intent(in) :: rscale1_starts(nvcount+1)
  real*8, intent(in) :: center1(3,0:*)
  integer, intent(in) :: center1_offsets(0:*)
  integer, intent(in) :: center1_starts(nvcount+1)
  complex*16, intent(in) :: expn1(0:nterms1,-(nterms1):nterms1,0:*)
  integer, intent(in) :: expn1_offsets(0:*)
  integer, intent(in) :: expn1_starts(nvcount+1)
  integer, intent(in) :: nterms1
  real*8, intent(in) :: rscale2(nvcount)
  real*8, intent(in) :: center2(3,nvcount)
  complex*16 expn2(0:nterms2,-(nterms2):nterms2,nvcount)
  !f2py intent(in,out) expn2
  complex*16 :: expn2_tmp(0:nterms2, -(nterms2):nterms2)
  integer, intent(in) :: nterms2
  real*8, intent(in) :: radius(nvcount)
  real*8, intent(in) :: xnodes(nquad)
  real*8, intent(in) :: wts(nquad)
  integer, intent(in) :: nquad
  integer ier(nvcount)
  !f2py intent(in,out) ier
  integer :: ier_tmp

  if (nvcount .le. 10) then
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dloclocquadu(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) +      &
          icsr)), center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,&
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          radius(ivcount), xnodes, wts, nquad, ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
  else
    !$omp parallel do default(none) schedule(dynamic, 10) private(icsr, ncsr_count,&
    !$omp expn2_tmp, ier_tmp) shared(nvcount, zk, rscale1, rscale1_offsets,        &
    !$omp rscale1_starts, center1, center1_offsets, center1_starts, expn1,         &
    !$omp expn1_offsets, expn1_starts, nterms1, rscale2, center2, expn2, nterms2,  &
    !$omp radius, xnodes, wts, nquad, ier)
    do ivcount = 1, nvcount
      ncsr_count = rscale1_starts(ivcount+1) - rscale1_starts(ivcount)
      do icsr = 0, ncsr_count-1
        ier_tmp = 0
        call h3dloclocquadu(zk, rscale1(rscale1_offsets(rscale1_starts(ivcount) +      &
          icsr)), center1(1, center1_offsets(center1_starts(ivcount) + icsr)), expn1(0,&
          -(nterms1), expn1_offsets(expn1_starts(ivcount) + icsr)), nterms1,           &
          rscale2(ivcount), center2(1, ivcount), expn2_tmp(0, -(nterms2)), nterms2,    &
          radius(ivcount), xnodes, wts, nquad, ier_tmp)
        expn2(:, :, ivcount) = expn2(:, :, ivcount) + expn2_tmp
        ier(ivcount) = max(ier(ivcount), ier_tmp)
      enddo
    enddo
    !$omp end parallel do
  endif
  return
end

! vim: filetype=fortran
import logging

from apps.elt.enum import ELTStatus
from apps.elt.models import ELTDevice, ELTStand, ELTSystem, FullELTVersion
from apps.network_access.models import Stand, System

logger = logging.getLogger(__name__)


class UpdateStructuresUseCase:
    def execute(self) -> None:
        try:
            version = FullELTVersion.objects.filter(status=ELTStatus.ACTUAL).latest('created_at')
        except FullELTVersion.DoesNotExist:
            return

        self._sync_systems(version)
        self._sync_stands(version)

    def _sync_systems(self, version: FullELTVersion) -> None:
        synced_cis: set[str] = set()

        for elt_system in ELTSystem.objects.filter(version=version):
            try:
                System.objects.update_or_create(
                    ci=elt_system.ci,
                    defaults={
                        'name': elt_system.name,
                        'is_it_service': bool(elt_system.is_it_service),
                        'is_active': True,
                    },
                )
                synced_cis.add(elt_system.ci)
            except Exception:
                logger.exception('Error syncing system ci=%s', elt_system.ci)

        System.objects.exclude(ci__in=synced_cis).update(is_active=False)

    def _sync_stands(self, version: FullELTVersion) -> None:
        synced_cis: set[str] = set()

        for elt_stand in ELTStand.objects.filter(version=version).select_related('system'):
            try:
                system = System.objects.get(ci=elt_stand.system.ci)
                Stand.objects.update_or_create(
                    ci=elt_stand.ci,
                    defaults={
                        'name': elt_stand.name or '',
                        'has_anonymized_data': elt_stand.sb_security_group == 't',
                        'ips': self._resolve_ips(elt_stand, version),
                        'is_active': True,
                        'system': system,
                    },
                )
                synced_cis.add(elt_stand.ci)
            except Exception:
                logger.exception('Error syncing stand ci=%s', elt_stand.ci)

        Stand.objects.exclude(ci__in=synced_cis).update(is_active=False)

    def _resolve_ips(self, elt_stand: ELTStand, version: FullELTVersion) -> list[str]:
        if not elt_stand.devices:
            return []
        device_cis = [ci.strip() for ci in elt_stand.devices.split(';') if ci.strip()]
        ips: list[str] = []
        for device in ELTDevice.objects.filter(ci__in=device_cis, version=version):
            if device.ips:
                ips.extend(ip.strip() for ip in device.ips.split(';') if ip.strip())
        return ips

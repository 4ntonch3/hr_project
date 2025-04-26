from apps.network_access.domain.protocols import SupportedProtocol
from apps.network_access.use_cases.create_network_interaction.domain.repository_interface import (
    ICreateNetworkInteractionRepository,
)


class CreateNetworkInteractionError(Exception):
    def __init__(self, details: str) -> None:
        super().__init__(details)

        self.details = details


class NoSuchNetworkZoneError(CreateNetworkInteractionError):
    pass


class NoProtocolError(CreateNetworkInteractionError):
    pass


class NoPortsError(CreateNetworkInteractionError):
    pass


class WrongProtocolError(CreateNetworkInteractionError):
    pass


class WrongPortError(CreateNetworkInteractionError):
    pass


class CreateNetworkInteractionUseCase:
    def __init__(self, repo: ICreateNetworkInteractionRepository) -> None:
        self._repo = repo

    def execute(
        self,
        arch_interaction_guid: str,
        src_arch_stand_guid: str,
        src_arch_component_guid: str,
        dst_arch_stand_guid: str,
        dst_arch_component_guid: str,
        src_network_zone_name: str,
        dst_network_zone_name: str,
        protocol_to_ports: dict[str, list[str]],
        user_id: int,
    ) -> str:
        network_zone_name_2_id = self._repo.get_network_zone_id_by_name(
            network_zones_names=[src_network_zone_name, dst_network_zone_name]
        )

        try:
            src_network_zone_id = network_zone_name_2_id[src_network_zone_name]
        except KeyError:
            raise NoSuchNetworkZoneError(f'Не найдено Сетевой Зоны с именем `{src_network_zone_name}`')

        try:
            dst_network_zone_id = network_zone_name_2_id[dst_network_zone_name]
        except KeyError:
            raise NoSuchNetworkZoneError(f'Не найдено Сетевой Зоны с именем `{dst_network_zone_name}`')

        self._validate_protocol_to_ports(protocol_to_ports)

        creation_reason = (
            f'Создано по инициативе пользователя с ID `{user_id}` в рамках создания Сетевого Взаимодействия'
        )
        with self._repo.transaction:
            src_ag_id = self._repo.create_access_group(
                src_arch_stand_guid,
                src_arch_component_guid,
                src_network_zone_id,
                creation_reason,
            )
            dst_ag_id = self._repo.create_access_group(
                dst_arch_stand_guid,
                dst_arch_component_guid,
                dst_network_zone_id,
                creation_reason,
            )

            ni_public_id = self._repo.create_network_interaction(
                src_network_zone_id,
                dst_network_zone_id,
                src_ag_id,
                dst_ag_id,
                arch_interaction_guid,
                protocol_to_ports,
                user_id,
                creation_reason,
            )

        return ni_public_id

    def _validate_protocol_to_ports(self, protocol_to_ports: dict[str, list[str]]) -> None:
        if not protocol_to_ports:
            raise NoProtocolError('Не указано ни одного протокола')

        for protocol, ports in protocol_to_ports.items():
            if protocol not in SupportedProtocol:
                raise WrongProtocolError(f'Протокол `{protocol}` не входит в список поддерживаемых')
            if not ports:
                raise NoPortsError(f'Для протокола `{protocol}` не указан ни один порт')

            for port in ports:
                self._validate_port(self, protocol, port)

    def _validate_port(self, protocol: str, port: str) -> None:
        try:
            int(port)
        except ValueError:
            raise WrongPortError(f'Некорректный порт `{port}` у протокола `{protocol}`')

        port = int(port)

        if 1 <= port <= 65536:
            return

        raise WrongPortError(f'Некорректный порт `{port}` у протокола `{protocol}`')

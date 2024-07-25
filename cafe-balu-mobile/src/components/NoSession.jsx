import { StyleSheet, Text, View } from 'react-native';
import React, { useState } from 'react';
import { emptyImg } from '../../assets/imgs';
import { Image } from '@rneui/base';
import { Button } from '@rneui/base';
import ModalLogin from './ModalLogin';

export default function NoSession({ setReload }) {
    const [showModal, setShowModal] = useState(false);

    return (
        <View style={styles.centerNull}>
            <Text style={styles.null}>Para ver este contenido debes iniciar sesión</Text>
            <Button
                onPress={() => setShowModal(true)}
                title="Iniciar sesión"
                buttonStyle={styles.loginButton}
                containerStyle={styles.buttonContainer}
            />
            <Image
                source={{ uri: emptyImg }}
                style={styles.notFound}
                resizeMode="contain"
            />
            <ModalLogin visible={showModal} setVisible={setShowModal} setReload={setReload} />
        </View>
    );
}

const styles = StyleSheet.create({
    centerNull: {
        justifyContent: 'center',
        alignItems: 'center',
        flex: 1,
    },
    notFound: {
        width: 400,
        height: 400,
    },
    null: {
        fontSize: 24,
        fontWeight: 'bold',
        textAlign: 'center',
        color: '#8C8B8A',
        marginTop: 125,
        marginBottom: 25
    },
    loginButton: {
        backgroundColor: '#A77B4A',
        borderRadius: 10,
    },
    buttonContainer: {
        width: '50%',
        alignSelf: 'center',
        marginTop: 20,
    },
});